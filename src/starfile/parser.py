from __future__ import annotations

import linecache
from collections import deque
from io import StringIO
from linecache import getline
import shlex

import numpy as np
import pandas as pd
from pathlib import Path
from typing import TYPE_CHECKING, Union, Optional, Dict, Tuple, List

from starfile.typing import DataBlock

if TYPE_CHECKING:
    from os import PathLike


class StarParser:
    filename: Path
    n_lines_in_file: int
    n_blocks_to_read: int
    current_line_number: int
    data_blocks: Dict[DataBlock]
    parse_as_string: List[str]

    def __init__(
        self,
        filename: PathLike,
        n_blocks_to_read: Optional[int] = None,
        parse_as_string: List[str] = [],
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

        # parse file
        self.current_line_number = 0
        self.parse_file()
        linecache.clearcache()

    @property
    def current_line(self) -> str:
        return getline(str(self.filename), self.current_line_number).strip()

    def parse_file(self):
        while self.current_line_number <= self.n_lines_in_file:
            if len(self.data_blocks) == self.n_blocks_to_read:
                break
            elif self.current_line.startswith('data_'):
                block_name, block = self._parse_data_block()
                self.data_blocks[block_name] = block
            else:
                self.current_line_number += 1

    def _parse_data_block(self) -> Tuple[str, DataBlock]:
        # current line starts with 'data_foo'
        block_name = self.current_line[5:]  # 'data_foo' -> 'foo'

        # iterate over file,
        while self.current_line_number <= self.n_lines_in_file:
            self.current_line_number += 1
            if self.current_line.startswith('loop_'):
                return block_name, self._parse_loop_block()
            elif self.current_line.startswith('_'):  # line is simple block
                return block_name, self._parse_simple_block()

    def _parse_simple_block(self) -> Dict[str, Union[str, int, float]]:
        block = {}
        while self.current_line_number <= self.n_lines_in_file:
            if self.current_line.startswith('data'):
                break
            elif self.current_line.startswith('_'):  # '_foo bar'
                k, v = shlex.split(self.current_line)
                column_name = k[1:]
                parse_column_as_string = (
                    self.parse_as_string is not None
                    and any(column_name == col for col in self.parse_as_string)
                )
                if parse_column_as_string is True:
                    block[column_name] = v
                else:
                    block[column_name] = numericise(v)
            self.current_line_number += 1
        return block

    def _parse_loop_block(self) -> pd.DataFrame:
        # parse loop header
        loop_column_names = deque()
        self.current_line_number += 1

        while self.current_line.startswith('_'):
            column_name = self.current_line.split()[0][1:]
            loop_column_names.append(column_name)
            self.current_line_number += 1

        # skip empty lines 
        while self.current_line.strip() == '':
            self.current_line_number += 1
            if self.current_line_number > self.n_lines_in_file:
                break

        # now parse the loop block data
        loop_data = deque()
        while self.current_line_number <= self.n_lines_in_file:
            if self.current_line.startswith('data_'):
                break
            loop_data.append(self.current_line)
            self.current_line_number += 1
        loop_data = '\n'.join(loop_data)
        if loop_data[-2:] != '\n':
            loop_data += '\n'

        # put string data into a dataframe
        if loop_data.startswith('\n'):
            n_cols = len(loop_column_names)
            df = pd.DataFrame(np.zeros(shape=(0, n_cols)))
            df.columns = loop_column_names
        else:
            column_name_to_index = {col: idx for idx, col in enumerate(loop_column_names)}
            df = pd.read_csv(
                StringIO(loop_data.replace("'", '"')),
                delimiter=r'\s+',
                header=None,
                comment='#',
                dtype={column_name_to_index[k]: str for k in self.parse_as_string if k in loop_column_names},
                keep_default_na=False,
                na_values=['nan','NaN','<NA>'],
                engine='c',
            )
            df.columns = loop_column_names

            # Numericise all columns in temporary copy
            df_numeric = df.apply(_apply_numeric)

            # Replace columns that are all NaN with the original columns
            df_numeric[df_numeric.columns[df_numeric.isna().all()]] = df[df_numeric.columns[df_numeric.isna().all()]]

            # Replace columns that should be strings
            for col in df.columns:
                df[col] = df_numeric[col] if col not in self.parse_as_string else df[col]
        return df


def count_lines(file: Path) -> int:
    with open(file, 'rb') as f:
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


def _apply_numeric(col: pd.Series) -> pd.Series:
    try:
        return pd.to_numeric(col)
    except ValueError:
        return col
