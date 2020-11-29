from linecache import getline
from collections import OrderedDict
from io import StringIO

import pandas as pd
from pathlib import Path
from typing import List, Union


class StarParser:
    def __init__(self, filename: Union[str, Path], read_n_blocks=None):
        # set filename, with path checking
        self.filename = filename

        # initialise attributes for parsing
        self._dataframes = OrderedDict()
        self._initialise_n_lines()
        self._current_line_number = 0
        self._current_dataframe_index = 0
        self._clear_buffer()
        self.read_n_blocks = read_n_blocks

        # parse file
        self.parse_file()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename: Union[str, Path]):
        filename = Path(filename)
        if filename.exists():
            self._filename = filename
        else:
            raise FileNotFoundError

    @property
    def n_lines(self):
        return self._n_lines

    def _initialise_n_lines(self):
        with open(self.filename, 'rb') as f:
                self._n_lines = sum(1 for line in f)

    @property
    def current_line_number(self):
        return self._current_line_number

    @property
    def current_line(self):
        return self._get_line(self.current_line_number)

    def _get_line(self, line_number: int):
        return getline(str(self.filename), line_number).strip()

    def _next_line(self):
        self._current_line_number += 1

    @property
    def buffer(self):
        return self._buffer

    def _clear_buffer(self):
        self._buffer = ""

    def _add_line_to_buffer(self, line):
        self._buffer += f'{line}\n'

    def _add_current_line_to_buffer(self):
        self._add_line_to_buffer(self.current_line)

    @property
    def buffer_split_on_newline(self):
        return self.buffer.split('\n')

    @property
    def dataframes(self):
        return self._dataframes

    def _add_dataframe(self, df: pd.DataFrame):
        key = self._get_dataframe_key(df)
        self.dataframes[key] = df
        self._increment_dataframe_index()

    @property
    def current_datablock_name(self):
        return self._current_data_block_name

    @current_datablock_name.setter
    def current_datablock_name(self, name: str):
        self._current_data_block_name = name

    @property
    def current_dataframe_index(self):
        return self._current_dataframe_index

    def _increment_dataframe_index(self):
        self._current_dataframe_index += 1

    def _get_dataframe_key(self, df):
        if df.name == '' or df.name in self.dataframes.keys():
            return self._current_dataframe_index
        else:
            return df.name

    def parse_file(self):
        while self.current_line_number <= self.n_lines:
            if len(self.dataframes) == self.read_n_blocks:
                break

            elif self.current_line.startswith('data_'):
                self._parse_data_block()

            if not self.current_line.startswith('data_'):
                self._next_line()

        self._to_numeric()
        return

    def _parse_data_block(self):
        # store data block name
        self.current_datablock_name = self.current_line[5:]

        # iterate over lines in each block and process as keywords are reached
        while self.current_line_number <= self.n_lines:
            self._next_line()

            if self.current_line.startswith('loop_'):
                self._parse_loop_block()
                return

            elif self.current_line.startswith('data_') or self.current_line_number == self.n_lines:
                self._parse_simple_block_from_buffer()
                return

            self._add_current_line_to_buffer()
        return

    def _parse_simple_block_from_buffer(self):
        # tidy up buffer
        data = self._clean_simple_block_buffer()

        # make dataframe
        df = self._cleaned_simple_block_to_dataframe(data)

        # set dataframe name
        df.name = self._current_data_block_name

        # add dataframe
        self._add_dataframe(df)

    def _clean_simple_block_buffer(self):
        clean_datablock = {}

        for line in self.buffer_split_on_newline:
            if line == '' or line.startswith('#'):
                continue

            heading_name = line.split()[0][1:]
            value = line.split()[1]
            clean_datablock[heading_name] = value

        return clean_datablock

    def _cleaned_simple_block_to_dataframe(self, data: dict):
        return pd.DataFrame(data, columns=data.keys(), index=[0])

    def _parse_loop_block(self):
        self._next_line()
        header = self._parse_loop_header()
        df = self._parse_loop_data()
        df.columns = header
        df.name = self._current_data_block_name
        self._add_dataframe(df)
        return

    def _parse_loop_header(self) -> List:
        self._clear_buffer()

        while self.current_line.startswith('_'):
            heading = self.current_line.split()[0][1:]
            self._add_line_to_buffer(heading)
            self._next_line()

        header = self.buffer.split()
        return header

    def _parse_loop_data(self) -> pd.DataFrame:
        self._clear_buffer()

        while self.current_line_number <= self.n_lines:
            if self.current_line.startswith('data_'):
                break
            self._add_current_line_to_buffer()
            self._next_line()

        df = pd.read_csv(StringIO(self.buffer), delim_whitespace=True, header=None, comment='#')
        return df

    def _to_numeric(self):
        for key, df in self.dataframes.items():
            # applying pd.to_numeric loses name dataframes of DataFrame, need to extract and reapply here
            name = getattr(df, 'name', None)

            # to numeric
            self.dataframes[key] = df.apply(pd.to_numeric, errors='ignore')

            # reapply name
            if name is not None:
                self.dataframes[key].name = name








