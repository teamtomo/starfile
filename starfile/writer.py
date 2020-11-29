import datetime
from pathlib import Path
from typing import Union

import pandas as pd

from .version import __version__


class StarWriter:
    def __init__(self, dataframes: Union[pd.DataFrame, dict, list], filename: Union[Path, str],
                 overwrite=False):
        self.overwrite = overwrite
        self.filename = filename
        self.dataframes = dataframes

    @property
    def dataframes(self):
        return self._dataframes

    @dataframes.setter
    def dataframes(self, dataframes: Union[pd.DataFrame, dict, list]):
        if isinstance(dataframes, pd.DataFrame):
            self._dataframes = self.coerce_dataframe(dataframes)
        elif isinstance(dataframes, dict):
            self._dataframes = self.coerce_dict(dataframes)
        elif isinstance(dataframes, list):
            self._dataframes = self.coerce_list(dataframes)
        else:
            raise ValueError(f'Expected a DataFrame, dict or list object, got {type(dataframes)}')

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename: Union[Path, str]):
        self.filename = Path(filename)
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

    @property
    def buffer(self):
        return self._buffer

    def clear_buffer(self):
        self._buffer = ""

    def add_line_to_buffer(self, line):
        self._buffer += f'{line}\n'

    def add_comment_to_buffer(self, line):
        self.add_line_to_buffer(f'# {line}')

    def add_blank_line_to_buffer(self):
        self.add_line_to_buffer('')

    def add_blank_lines_to_buffer(self, n: int):
        for i in range(n):
            self.add_blank_line_to_buffer()

    def _write_buffer_to_disk(self):
        with open(self.filename, 'a+') as file:
            file.write(self.buffer)

    def _write_buffer_and_clear(self):
        self._write_buffer_to_disk()
        self.clear_buffer()

    def add_package_info_to_buffer(self):
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        line = f'Created by the starfile Python package (version {__version__}) on {now}\n'
        self.add_comment_to_buffer(line)

    def write_package_info(self):
        self.add_package_info_to_buffer()
        self._write_buffer_and_clear()

    def write_star_file(self, filename: str = None, **kwargs):
        self.write_package_info()

        for _, df in self.dataframes.items():
            self._write_data_block(df, filename, **kwargs)

        self.add_blank_lines_to_buffer(2)
        self._write_buffer_and_clear()
        return

    def add_loopheader_to_buffer(self, df: pd.DataFrame):
        self.add_line_to_buffer('loop_')
        headings = [f'_{column_name} #{idx}' for idx, column_name in
                    enumerate(df.columns, 1)]
        for heading in headings:
            self.add_line_to_buffer(heading)

    def _write_loopheader(self, df: pd.DataFrame):
        self.add_loopheader_to_buffer(df)
        self._write_buffer_and_clear()

    def get_block_name(self, df: pd.DataFrame):
        return 'data_' + getattr(df, 'name')

    def add_block_name_to_buffer(self, df: pd.DataFrame):
        self.add_line_to_buffer(self.get_block_name(df))

    def _write_data_block(self, df: pd.DataFrame):
        self.add_block_name_to_buffer(df)

        if df.shape[0] == 1:
            self._write_simple_block(df)
        elif df.shape[0] > 1:
            self._write_loop_block(df)
        self._write_blank_lines( 2)
        return

    def _write_simple_block(self, dataframe: pd.DataFrame, filename: str):
        entries = [f'_{column_name}\t\t\t{dataframe[column_name][0]}' for column_name in
                   dataframe.columns]

        with open(filename, 'a') as file:
            for entry in entries:
                file.write(f'{entry}\n')
        return

    def _write_blank_lines(self, filename: str, n: int):
        with open(filename, 'a') as file:
            for i in range(n):
                file.write('\n')
        return

    def _write_loop_block(self, dataframe: pd.DataFrame, filename: str, **kwargs):
        self._write_loopheader(dataframe, filename)

        # new main block
        if 'float_format' not in kwargs.keys():
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False,
                             float_format='%.8f', **kwargs)
        else:
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, **kwargs)
        return
