from __future__ import annotations

import shlex
from collections import deque
from functools import lru_cache
from io import StringIO
from linecache import getline
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import numpy as np
import pandas as pd
import polars as pl

from starfile.typing import DataBlock

if TYPE_CHECKING:
    from os import PathLike


class StarParser:
    filename: Path
    n_lines_in_file: int
    n_blocks_to_read: int
    current_line_number: int
    data_blocks: dict[DataBlock]
    parse_as_string: list[str]

    def __init__(
        self,
        filename: PathLike,
        n_blocks_to_read: Optional[int] = None,
        parse_as_string: list[str] = [],
        polars: bool = False,
    ):
        # set filename, with path checking
        filename = Path(filename)
        if not filename.exists():
            raise FileNotFoundError(filename)
        self.filename = filename

        # setup for parsing
        self.data_blocks = {}
        self.n_lines_in_file = count_lines(self.filename)
        self.n_blocks_to_read = n_blocks_to_read
        self.parse_as_string = parse_as_string

        self.polars = polars

        # parse file
        self.current_line_number = 0
        self.parse_file()

    @lru_cache(maxsize=25)
    def _get_line(self, line_number: int) -> str:
        return " ".join(getline(str(self.filename), line_number).split())

    def parse_file(self):
        while self.current_line_number <= self.n_lines_in_file:
            if len(self.data_blocks) == self.n_blocks_to_read:
                break
            elif self._get_line(self.current_line_number).startswith("data_"):
                block_name, block = self._parse_data_block()
                self.data_blocks[block_name] = block
            else:
                self.current_line_number += 1

    def _parse_data_block(self) -> tuple[str, DataBlock]:
        # current line starts with 'data_foo'
        block_name = self._get_line(self.current_line_number)[5:]  # 'data_foo' -> 'foo'
        self.current_line_number += 1

        # iterate over file,
        while self.current_line_number <= self.n_lines_in_file:
            self.current_line_number += 1
            current_line = self._get_line(self.current_line_number)
            if current_line.startswith("loop_"):
                return block_name, self._parse_loop_block()
            elif current_line.startswith("_"):  # line is simple block
                return block_name, self._parse_simple_block()

    def _parse_simple_block(self) -> dict[str, Union[str, int, float]]:
        block = {}
        while self.current_line_number <= self.n_lines_in_file:
            c = self._get_line(self.current_line_number)
            if c.startswith("data"):
                break
            elif c.startswith("_"):  # '_foo bar'
                k, v = shlex.split(c)
                column_name = k[1:]
                parse_column_as_string = self.parse_as_string is not None and any(
                    column_name == col for col in self.parse_as_string
                )
                if parse_column_as_string is True:
                    block[column_name] = v
                else:
                    block[column_name] = numericise(v)
            self.current_line_number += 1
        return block

    def _parse_loop_block(self) -> pd.DataFrame | pl.DataFrame:
        # parse loop header
        loop_column_names = deque()
        self.current_line_number += 1

        while self._get_line(self.current_line_number).startswith("_"):
            column_name = self._get_line(self.current_line_number).split()[0][1:]
            loop_column_names.append(column_name)
            self.current_line_number += 1

        # now parse the loop block data
        loop_data = deque()
        while self.current_line_number <= self.n_lines_in_file:
            current_line = self._get_line(self.current_line_number)
            if current_line.startswith("data_"):
                break
            previous_line = self._get_line(self.current_line_number - 1)
            if not (current_line.isspace() and previous_line.isspace()) and (
                current_line and previous_line
            ):
                loop_data.append(current_line)
            self.current_line_number += 1
        loop_data = "\n".join(loop_data)
        if loop_data[-2:] != "\n":
            loop_data += "\n"

        # put string data into a dataframe
        if loop_data == "\n":
            n_cols = len(loop_column_names)
            df = pl.DataFrame(np.zeros(shape=(0, n_cols)))
        else:
            df = pl.read_csv(
                StringIO(loop_data.replace("'", '"')),
                separator=" ",
                has_header=False,
                comment_prefix="#",
                dtypes={
                    k: pl.String for k in self.parse_as_string if k in loop_column_names
                },
                truncate_ragged_lines=True,
                null_values=["", "<NA>"],
            )
            df.columns = loop_column_names

            # If the column type is string then use empty strings rather than null
            df = df.with_columns(pl.col(pl.String).fill_null(""))

            # Replace columns that should be strings
            for col in df.columns:
                if col in self.parse_as_string:
                    df = df.with_columns(
                        pl.col(col).cast(pl.String).fill_null("").alias(col)
                    )
        if self.polars:
            return df
        return df.to_pandas()


def count_lines(file: Path) -> int:
    with open(file, "rb") as f:
        return sum(1 for _ in f)


def block_name_from_line(line: str) -> str:
    """'data_general' -> 'general'"""
    return line[5:]


def heading_from_line(line: str) -> str:
    """'_rlnSpectralIndex #1' -> 'rlnSpectralIndex'."""
    return line.split()[0][1:]


def numericise(value: str) -> Union[str, int, float]:
    try:
        # Try to convert the string value to an integer
        value = int(value)
    except ValueError:
        try:
            # If it's not an integer, try to convert it to a float
            value = float(value)
        except ValueError:
            # If it's not a float either, leave it as a string
            value = value
    return value
