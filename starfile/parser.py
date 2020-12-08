from collections import OrderedDict
from io import StringIO

import pandas as pd
from pathlib import Path
from typing import List, Union

from .core import TextBuffer, TextCrawler


class StarParser:
    def __init__(self, filename: Union[str, Path], read_n_blocks=None):
        # set filename, with path checking
        self.filename = filename

        # initialise attributes for parsing
        self.text_buffer = TextBuffer()
        self.crawler = TextCrawler(self.filename)
        self.read_n_blocks = read_n_blocks
        self._dataframes = OrderedDict()
        self._current_dataframe_index = 0
        self._initialise_n_lines()

        # parse file
        self.parse_file()

    def parse_file(self):
        while self.crawler.current_line_number <= self.n_lines:
            if len(self.dataframes) == self.read_n_blocks:
                break

            elif self.crawler.current_line.startswith('data_'):
                self._parse_data_block()

            if not self.crawler.current_line.startswith('data_'):
                self.crawler.increment_line_number()

        self.dataframes_to_numeric()
        return

    def _parse_data_block(self):
        self.current_block_name = self._block_name_from_current_line()

        while self.crawler.current_line_number <= self.n_lines:
            self.crawler.increment_line_number()
            line = self.crawler.current_line

            if line.startswith('loop_'):
                self._parse_loop_block()
                return

            elif line.startswith('data_') or self.crawler.current_line_number == self.n_lines:
                self._parse_simple_block()
                return

            self.text_buffer.add_line(line)
        return

    def _parse_simple_block(self):
        data = self._clean_simple_block_in_buffer()

        df = self._cleaned_simple_block_to_dataframe(data)
        df.name = self._current_data_block_name

        self._add_dataframe(df)

    def _parse_loop_block(self):
        self.crawler.increment_line_number()
        header = self._parse_loop_header()
        df = self._parse_loop_data()
        df.columns = header
        df.name = self._current_data_block_name
        self._add_dataframe(df)
        return

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
        self._n_lines = self.crawler.count_lines()

    @property
    def dataframes(self):
        return self._dataframes

    def _add_dataframe(self, df: pd.DataFrame):
        key = self._get_dataframe_key(df)
        self.dataframes[key] = df
        self._increment_dataframe_index()

    @property
    def current_block_name(self):
        return self._current_data_block_name

    @current_block_name.setter
    def current_block_name(self, name: str):
        self._current_data_block_name = name

    @property
    def current_dataframe_index(self):
        return self._current_dataframe_index

    def _increment_dataframe_index(self):
        self._current_dataframe_index += 1

    def _get_dataframe_key(self, df):
        name = df.name

        if name == '' or isinstance(name, int) or name in self.dataframes.keys():
            return self._current_dataframe_index
        else:
            return df.name

    def _clean_simple_block_in_buffer(self):
        clean_datablock = {}

        for line in self.text_buffer.buffer:
            if line == '' or line.startswith('#'):
                continue

            heading_name = self.heading_from_line(line)
            value = line.split()[1]
            clean_datablock[heading_name] = value

        return clean_datablock

    @staticmethod
    def _cleaned_simple_block_to_dataframe(data: dict):
        return pd.DataFrame(data, columns=data.keys(), index=[0])

    def _parse_loop_header(self) -> List:
        self.text_buffer.clear()

        while self.crawler.current_line.startswith('_'):
            heading = self.heading_from_line(self.crawler.current_line)
            self.text_buffer.add_line(heading)
            self.crawler.increment_line_number()

        return self.text_buffer.buffer

    def _parse_loop_data(self) -> pd.DataFrame:
        self.text_buffer.clear()

        while self.crawler.current_line_number <= self.n_lines:
            current_line = self.crawler.current_line
            if current_line.startswith('data_'):
                break
            self.text_buffer.add_line(current_line)
            self.crawler.increment_line_number()

        df = pd.read_csv(StringIO(self.text_buffer.as_str()), delim_whitespace=True, header=None,
                         comment='#')
        return df

    def dataframes_to_numeric(self):
        """
        Converts strings in dataframes into numerical values where possible

        applying pd.dataframes_to_numeric loses name dataframes of DataFrame,
        need to extract name and reapply inline
        """
        for key, df in self.dataframes.items():
            name = getattr(df, 'name', None)
            self.dataframes[key] = df.apply(pd.to_numeric, errors='ignore')
            if name is not None:
                self.dataframes[key].name = name

    @staticmethod
    def _block_name_from_line(line: str):
        return line[5:]

    def _block_name_from_current_line(self):
        return self._block_name_from_line(self.crawler.current_line)

    @staticmethod
    def heading_from_line(line: str):
        return line.split()[0][1:]

    @property
    def first_dataframe(self):
        return self.dataframe_at_index(0)

    def dataframe_at_index(self, idx: int):
        return self.dataframes_as_list()[idx]

    def dataframes_as_list(self):
        return list(self.dataframes.values())




