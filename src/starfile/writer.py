"""Module for writing STAR file format."""

from __future__ import annotations

import csv
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator

import pandas as pd

if TYPE_CHECKING:
    from os import PathLike

    from .typing import DataBlock

from .utils import TextBuffer

__version__ = version("starfile")


class StarWriter:
    """Writer object for handling STAR file writing.

    Attributes
    ----------
    data_blocks : DataBlock | dict[str, DataBlock] | list[DataBlock]
        The data blocks to be written to the STAR file.
    filename : Optional[PathLike]
        The path to the output file.
    float_format : str
        The format string for floating-point numbers. By default "%.6f".
    separator : str | None
        The separator to use between columns. If None, then fixed-width columns are
        written. Otherwise, the provided string is used as the separator. By default
        None.
    na_rep : str
        The string to use for missing values. By default "<NA>".
    quote_character : str
        The character to use for quoting strings. By default '"'.
    quote_all_strings : bool
        Whether to quote all strings. By default False.
    """

    def __init__(
        self,
        data_blocks: DataBlock | dict[str, DataBlock] | list[DataBlock],
        filename: PathLike | None = None,
        float_format: str = "%.6f",
        separator: str | None = None,
        na_rep: str = "<NA>",
        quote_character: str = '"',
        quote_all_strings: bool = False,
    ) -> None:
        # coerce data
        self.data_blocks = self.coerce_data_blocks(data_blocks)

        self.filename: Path | None = Path(filename) if filename is not None else None
        self.float_format = float_format
        self.sep = separator
        self.na_rep = na_rep
        self.quote_character = quote_character
        self.quote_all_strings = quote_all_strings
        self.buffer = TextBuffer()

    def coerce_data_blocks(
        self, data_blocks: DataBlock | list[DataBlock] | dict[str, DataBlock]
    ) -> dict[str, DataBlock]:
        """Take single, list of, or dict of data blocks and transform to dictionary."""
        if isinstance(data_blocks, pd.DataFrame):
            return coerce_dataframe(data_blocks)
        elif isinstance(data_blocks, dict):
            return coerce_dict(data_blocks)
        elif isinstance(data_blocks, list):
            return coerce_list(data_blocks)
        else:
            raise ValueError(
                f"Expected DataFrame, dict[str, DataFrame] or list[DataFrame], "
                f"got {type(data_blocks)}"
            )

    def lines(self) -> Generator[str, None, None]:
        """Generator for the lines in this .star file data."""
        yield package_info()
        yield ""
        yield ""
        yield from self.data_block_generator()

    def to_string(self) -> str:
        """Convert the .star file data to a string."""
        return "".join(line + "\n" for line in self.lines())

    def write(self) -> None:
        """Write the .star file data to the held 'filename' attribute."""
        if self.filename is None:
            raise ValueError("Cannot write nameless file!")
        self.filename.write_text(self.to_string())

    def data_block_generator(self) -> Generator[str, None, None]:
        """Generator to convert each held data block into string representations."""
        for block_name, block in self.data_blocks.items():
            if isinstance(block, dict):
                yield from simple_block(
                    block_name=block_name,
                    data=block,
                    quote_character=self.quote_character,
                    quote_all_strings=self.quote_all_strings,
                )
            elif isinstance(block, pd.DataFrame):
                yield from loop_block(
                    block_name=block_name,
                    df=block,
                    float_format=self.float_format,
                    separator=self.sep,
                    na_rep=self.na_rep,
                    quote_character=self.quote_character,
                    quote_all_strings=self.quote_all_strings,
                )


def coerce_dataframe(df: pd.DataFrame) -> dict[str, DataBlock]:
    """Coerce a pandas DataFrame into a dict of data blocks."""
    if hasattr(df, "name") and df.name:
        # if the DataFrame has a name, use it as the key
        return {df.name: df}
    return {"": df}


def coerce_dict(
    data_blocks: DataBlock | dict[str, DataBlock],
) -> dict[str, DataBlock]:
    """Coerce dict into dict of data blocks."""
    # check if data is already Dict[str, DataBlock]
    for _, v in data_blocks.items():
        if type(v) in (dict, pd.DataFrame):
            return data_blocks
    # coerce if not
    return {"": data_blocks}


def coerce_list(
    data_blocks: list[DataBlock],
) -> dict[str, DataBlock]:
    """Coerce a list of DataFrames into a dict."""
    return {f"{idx}": df for idx, df in enumerate(data_blocks)}


def package_info() -> str:
    """Return package info header line."""
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    return (
        "# Created by the starfile Python package "
        f"(version {__version__}) at {time} on {date}"
    )


def quote(
    x: Any, *, quote_character: str = '"', quote_all_strings: bool = False
) -> str:
    """Quote a value if it's a string meeting certain conditions."""
    if isinstance(x, str) and (quote_all_strings or " " in x or not x):
        return f"{quote_character}{x}{quote_character}"
    return str(x)


def simple_block(
    block_name: str,
    data: dict[str, str | int | float],
    quote_character: str = '"',
    quote_all_strings: bool = False,
) -> Generator[str, None, None]:
    """Generate lines for a simple (key-value) data block."""
    yield f"data_{block_name}"
    yield ""
    for k, v in data.items():
        quoted_value = quote(
            v, quote_character=quote_character, quote_all_strings=quote_all_strings
        )
        yield f"_{k}\t\t\t{quoted_value}"
    yield ""
    yield ""


def loop_block(
    block_name: str,
    df: pd.DataFrame,
    float_format: str = "%.6f",
    separator: str | None = None,
    na_rep: str = "<NA>",
    quote_character: str = '"',
    quote_all_strings: bool = False,
) -> Generator[str, None, None]:
    """Generator for producing lines of a loop block from a DataFrame.

    Parameters
    ----------
    block_name : str
        The name of the data block.
    df : pd.DataFrame
        The DataFrame to convert to a loop block.
    float_format : str, optional
        The format string for floating-point numbers, by default '%.6f'.
    separator : str | None, optional
        The separator to use between columns, by default None. When None, a fixed width
        separator is used across all columns.
    na_rep : str, optional
        The string to use for missing values, by default '<NA>'.
    quote_character : str, optional
        The character to use for quoting strings, by default '"'.
    quote_all_strings : bool, optional
        Whether to quote all strings, by default False.
    """
    ### Header
    yield f"data_{block_name}"
    yield ""
    yield "loop_"
    for idx, column_name in enumerate(df.columns, 1):
        yield f"_{column_name} #{idx}"

    ### Data
    quoted_df = df.map(
        lambda x: quote(
            x, quote_character=quote_character, quote_all_strings=quote_all_strings
        )
    )

    # Fixed-width output
    if separator is None:
        string_output = quoted_df.to_string(
            header=False,
            index=False,
            na_rep=na_rep,
            float_format=lambda x: float_format % x,
            max_rows=None,
            max_cols=None,
            line_width=None,
            max_colwidth=None,
            show_dimensions=False,
        )
    # Delimited output
    else:
        string_output = quoted_df.to_csv(
            header=False,
            index=False,
            na_rep=na_rep,
            sep=separator,
            quoting=csv.QUOTE_NONE,
            escapechar=None,
            lineterminator="",
        )

    yield from string_output.splitlines()

    yield ""
    yield ""
