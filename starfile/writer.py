from __future__ import annotations

from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Union, Dict, List

import pandas as pd
from pkg_resources import get_distribution

from .utils import TextBuffer

if TYPE_CHECKING:
    from os import PathLike

__version__ = get_distribution("starfile").version


class StarWriter:
    def __init__(self, dataframes: Union[pd.DataFrame, Dict[pd.DataFrame], List[pd.DataFrame]],
                 filename: PathLike, overwrite: bool = False, float_format: str = '%.6f',
                 sep: str = '\t', na_rep: str = '<NA>', force_loop: bool = False):
        self.overwrite = overwrite
        self.filename = filename
        self.dataframes = dataframes
        self.float_format = float_format
        self.sep = sep
        self.na_rep = na_rep
        self.force_loop = force_loop
        self.buffer = TextBuffer()
        self.write_star_file()

    @property
    def dataframes(self):
        """
        Ordered dictionary of pandas dataframes
        df.name defines the data block name
        """
        return self._dataframes

    @dataframes.setter
    def dataframes(self, dataframes: Union[pd.DataFrame, Dict[pd.DataFrame], List[pd.DataFrame]]):
        if isinstance(dataframes, pd.DataFrame):
            self._dataframes = self.coerce_dataframe(dataframes)
        elif isinstance(dataframes, dict):
            self._dataframes = self.coerce_dict(dataframes)
        elif isinstance(dataframes, list):
            self._dataframes = self.coerce_list(dataframes)
        else:
            raise ValueError(f'Expected a DataFrame, Dict or List object, got {type(dataframes)}')

    @staticmethod
    def coerce_dataframe(df: pd.DataFrame):
        name = getattr(df, 'name', '')
        if name != '':
            name = 0
        return {name: df}

    @staticmethod
    def coerce_dict(dfs: Dict[str, pd.DataFrame]):
        """
        This method ensures that dataframe names are updated based on dict keys
        """
        for key, df in dfs.items():
            df.name = str(key)
        return dfs

    def coerce_list(self, dfs: List[pd.DataFrame]):
        """
        This method coerces a list of DataFrames into a dict
        """
        return self.coerce_dict(OrderedDict([(idx, df) for idx, df in enumerate(dfs)]))

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename: Union[Path, str]):
        self._filename = Path(filename)
        if not self.file_writable:
            raise FileExistsError('to overwrite an existing file set overwrite=True')

    @property
    def file_exists(self):
        return self.filename.exists()

    @property
    def file_writable(self):
        if self.overwrite or (not self.file_exists):
            return True
        else:
            return False

    def write_package_info(self):
        date = datetime.now().strftime('%d/%m/%Y')
        time = datetime.now().strftime('%H:%M:%S')
        line = f'Created by the starfile Python package (version {__version__}) at {time} on' \
               f' {date}'
        self.buffer.add_comment(line)
        self.buffer.add_blank_lines(1)
        self.buffer.write_as_new_file_and_clear(self.filename)

    def write_star_file(self, filename: str = None):
        self.write_package_info()

        for _, df in self.dataframes.items():
            self.write_block(df)

        self.buffer.add_blank_line()
        self.buffer.append_to_file_and_clear(self.filename)

    def write_loopheader(self, df: pd.DataFrame):
        self.buffer.add_line('loop_')
        lines = [f'_{column_name} #{idx}' for idx, column_name in enumerate(df.columns, 1)]

        for line in lines:
            self.buffer.add_line(line)

        self.buffer.append_to_file_and_clear(self.filename)

    @staticmethod
    def get_block_name(df: pd.DataFrame):
        return 'data_' + getattr(df, 'name', '')

    def add_block_name_to_buffer(self, df: pd.DataFrame):
        self.buffer.add_line(self.get_block_name(df))
        self.buffer.add_blank_lines(1)
        self.buffer.append_to_file_and_clear(self.filename)

    def write_block(self, df: pd.DataFrame):
        self.add_block_name_to_buffer(df)

        if (df.shape[0] == 1) and not self.force_loop:
            self._write_simple_block(df)
        elif (df.shape[0] > 1) or self.force_loop:
            self._write_loop_block(df)
        self.buffer.add_blank_lines(2)
        self.buffer.append_to_file_and_clear(self.filename)

    def _write_simple_block(self, df: pd.DataFrame):
        lines = [f'_{column_name}\t\t\t{df[column_name].iloc[0]}'
                 for column_name in df.columns]
        for line in lines:
            self.buffer.add_line(line)
        self.buffer.append_to_file_and_clear(self.filename)

    def _write_loop_block(self, df: pd.DataFrame):
        self.write_loopheader(df)
        df.to_csv(self.filename, mode='a', sep=self.sep, header=False, index=False,
                  float_format=self.float_format, na_rep=self.na_rep)
