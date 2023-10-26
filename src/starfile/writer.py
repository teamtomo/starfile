from __future__ import annotations

from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

import pandas as pd

from .typing import DataBlock
from .utils import TextBuffer

if TYPE_CHECKING:
    from os import PathLike

__version__ = version("starfile")


class StarWriter:
    def __init__(
        self,
        data_blocks: DataBlock | dict[str, DataBlock] | list[DataBlock],
        filename: PathLike,
        float_format: str = "%.6f",
        separator: str = "\t",
        na_rep: str = "<NA>",
    ):
        # coerce data
        self.data_blocks = self.coerce_data_blocks(data_blocks)

        # write
        self.filename = Path(filename)
        self.float_format = float_format
        self.sep = separator
        self.na_rep = na_rep
        self.buffer = TextBuffer()
        self.backup_if_file_exists()
        self.write()

    def coerce_data_blocks(
        self, data_blocks: DataBlock | list[DataBlock] | dict[str, DataBlock]
    ) -> dict[str, DataBlock]:
        if isinstance(data_blocks, pd.DataFrame):
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
                    file=self.filename, block_name=block_name, data=block
                )
            elif isinstance(block, pd.DataFrame):
                write_loop_block(
                    file=self.filename,
                    block_name=block_name,
                    df=block,
                    float_format=self.float_format,
                    separator=self.sep,
                    na_rep=self.na_rep,
                )

    def backup_if_file_exists(self):
        if self.filename.exists():
            new_name = self.filename.name + "~"
            backup_path = self.filename.resolve().parent / new_name
            self.filename.rename(backup_path)


def coerce_dataframe(df: pd.DataFrame) -> dict[str, DataBlock]:
    return {"": df}


def coerce_dict(data_blocks: DataBlock | dict[str, DataBlock]) -> dict[str, DataBlock]:
    """Coerce dict into dict of data blocks."""
    # check if data is already Dict[str, DataBlock]
    for _k, v in data_blocks.items():
        if type(v) in (dict, pd.DataFrame):  #
            return data_blocks
    # coerce if not
    return {"": data_blocks}


def coerce_list(data_blocks: list[DataBlock]) -> dict[str, DataBlock]:
    """Coerces a list of DataFrames into a dict."""
    return {f"{idx}": df for idx, df in enumerate(data_blocks)}


def write_blank_lines(file: Path, n: int):
    with open(file, mode="a") as f:
        f.write("\n" * n)


def write_package_info(file: Path):
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    line = f"# Created by the starfile Python package \
    (version {__version__}) at {time} on {date}"
    with open(file, mode="w+") as f:
        f.write(f"{line}\n")


def write_simple_block(file: Path, block_name: str, data: dict[str, str | int | float]):
    formatted_lines = "\n".join([f"_{k}\t\t\t{v}" for k, v in data.items()])
    with open(file, mode="a") as f:
        f.write(f"data_{block_name}\n\n")
        f.write(formatted_lines)
        f.write("\n\n\n")


def write_loop_block(
    file: Path,
    block_name: str,
    df: pd.DataFrame,
    float_format: str = "%.6f",
    separator: str = "\t",
    na_rep: str = "<NA>",
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
    df.to_csv(
        path_or_buf=file,
        mode="a",
        sep=separator,
        header=False,
        index=False,
        float_format=float_format,
        na_rep=na_rep,
    )
    write_blank_lines(file, n=2)
