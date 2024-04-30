from __future__ import annotations

from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Union

import pandas as pd
import polars as pl

from .typing import DataBlock
from .utils import TextBuffer

if TYPE_CHECKING:
    from os import PathLike

__version__ = version("starfile")


class StarWriter:
    def __init__(
        self,
        data_blocks: Union[DataBlock, dict[str, DataBlock], list[DataBlock]],
        filename: PathLike,
        float_format: int = 6,
        separator: str = "\t",
        na_rep: str = "<NA>",
        quote_character: str = '"',
        quote_all_strings: bool = False,
    ):
        # coerce data
        self.data_blocks = self.coerce_data_blocks(data_blocks)

        # write
        self.filename = Path(filename)
        self.float_format = float_format
        self.sep = separator
        self.na_rep = na_rep
        self.quote_character = quote_character
        self.quote_all_strings = quote_all_strings
        self.buffer = TextBuffer()
        self.backup_if_file_exists()
        self.write()

    def coerce_data_blocks(
        self, data_blocks: Union[DataBlock, list[DataBlock], dict[str, DataBlock]]
    ) -> dict[str, DataBlock]:
        if isinstance(data_blocks, pd.DataFrame) or isinstance(
            data_blocks, pl.DataFrame
        ):
            return coerce_dataframe(data_blocks)
        elif isinstance(data_blocks, dict):
            return coerce_dict(data_blocks)
        elif isinstance(data_blocks, list):
            return coerce_list(data_blocks)
        else:
            raise ValueError(
                f"Expected \
                {pd.DataFrame}, \
                {Dict[str, pd.DataFrame]} \
                or {List[pd.DataFrame]}, \
                or {pl.DataFrame}, \
                {Dict[str, pl.DataFrame]} \
                or {List[pl.DataFrame]}, \
                got {type(data_blocks)}"
            )

    def write(self):
        write_package_info(self.filename)
        write_blank_lines(self.filename, n=2)
        self.write_data_blocks()

    def write_data_blocks(self):
        for block_name, block in self.data_blocks.items():
            if isinstance(block, dict):
                write_simple_block(
                    file=self.filename,
                    block_name=block_name,
                    data=block,
                    quote_character=self.quote_character,
                    quote_all_strings=self.quote_all_strings,
                )
            elif isinstance(block, pd.DataFrame) or isinstance(block, pl.DataFrame):
                write_loop_block(
                    file=self.filename,
                    block_name=block_name,
                    df=block,
                    float_format=self.float_format,
                    separator=self.sep,
                    na_rep=self.na_rep,
                    quote_character=self.quote_character,
                    quote_all_strings=self.quote_all_strings,
                )

    def backup_if_file_exists(self):
        if self.filename.exists():
            new_name = self.filename.name + "~"
            backup_path = self.filename.resolve().parent / new_name
            if backup_path.exists():
                backup_path.unlink()
            self.filename.rename(backup_path)


def coerce_dataframe(df: pd.DataFrame | pl.DataFrame) -> dict[str, DataBlock]:
    return {"": df}


def coerce_dict(
    data_blocks: Union[DataBlock, dict[str, DataBlock]]
) -> dict[str, DataBlock]:
    """Coerce dict into dict of data blocks."""
    # check if data is already Dict[str, DataBlock]
    for k, v in data_blocks.items():
        if type(v) in (dict, pd.DataFrame, pl.DataFrame):  #
            return data_blocks
    # coerce if not
    return {"": data_blocks}


def coerce_list(data_blocks: list[DataBlock]) -> dict[str, DataBlock]:
    """Coerces a list of DataFrames into a dict"""
    return {f"{idx}": df for idx, df in enumerate(data_blocks)}


def write_blank_lines(file: Path, n: int):
    with open(file, mode="a") as f:
        f.write("\n" * n)


def write_package_info(file: Path):
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    line = f"# Created by the starfile Python package (version {__version__}) at {time} on {date}"
    with open(file, mode="w+") as f:
        f.write(f"{line}\n")


def write_simple_block(
    file: Path,
    block_name: str,
    data: dict[str, Union[str, int, float]],
    quote_character: str = '"',
    quote_all_strings: bool = False,
):
    quoted_data = {
        k: f"{quote_character}{v}{quote_character}"
        if isinstance(v, str) and (quote_all_strings or " " in v or v == "")
        else v
        for k, v in data.items()
    }
    formatted_lines = "\n".join([f"_{k}\t\t\t{v}" for k, v in quoted_data.items()])
    with open(file, mode="a") as f:
        f.write(f"data_{block_name}\n\n")
        f.write(formatted_lines)
        f.write("\n\n\n")


def write_loop_block(
    file: Path,
    block_name: str,
    df: pd.DataFrame | pl.DataFrame,
    float_format: int = 6,
    separator: str = "\t",
    na_rep: str = "<NA>",
    quote_character: str = '"',
    quote_all_strings: bool = False,
):
    # write header
    header_lines = [
        f"_{column_name} #{idx}" for idx, column_name in enumerate(df.columns, 1)
    ]
    with open(file, mode="a") as f:
        f.write(f"data_{block_name}\n\n")
        f.write("loop_\n")
        f.write("\n".join(header_lines))
        f.write("\n")

    # write data
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    df = df.with_columns(
        pl.col(pl.String).map_elements(
            lambda x: f"{quote_character}{x}{quote_character}"
            if (quote_all_strings or " " in x or x == "")
            else x
        )
    )

    with open(file, "a") as fobj:
        df.write_csv(
            fobj,
            separator=separator,
            include_header=False,
            float_precision=float_format,
            null_value=na_rep,
            quote_style="never",
        )
    write_blank_lines(file, n=2)
