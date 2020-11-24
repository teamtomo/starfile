from linecache import getline
from io import StringIO

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Union

from .version import __version__


class StarFile:
    def __init__(self, filename: Union[str, Path] = None,
                 data: Union[pd.DataFrame, List[pd.DataFrame]] = None,
                 read_n_blocks=None):
        self.filename = filename
        self.dataframes = []
        self.line_number = 0
        if self.filename is not None:
            self.n_lines = None
        self.n_data_blocks = read_n_blocks

        if isinstance(data, pd.DataFrame) or isinstance(data, list):
            self._add_data(data)

        elif self.filename is not None:
            self.read_file()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename: Union[str, Path]):
        if isinstance(filename, (str, Path)) and Path(filename).exists():
            self._filename = Path(filename)
        else:
            self._filename = None

    @property
    def data(self):
        if len(self._dataframes) == 1 and isinstance(self._dataframes, list):
            return self._dataframes[0]
        return self.dataframes

    @property
    def dataframes(self):
        return self._dataframes

    @dataframes.setter
    def dataframes(self, dataframes: List[pd.DataFrame]):
        self._dataframes = dataframes

    def _add_dataframe(self, df: pd.DataFrame):
        self.dataframes.append(df)

    def _add_data(self, data: Union[pd.DataFrame, List[pd.DataFrame]]):
        if isinstance(data, pd.DataFrame):
            data = [data]
        for df in data:
            self._add_dataframe(df)
        return

    @property
    def n_lines(self):
        return self._n_lines

    @n_lines.setter
    def n_lines(self, value):
        if value is None and self.filename.exists():
            with open(self.filename, 'rb') as f:
                self._n_lines = sum(1 for line in f)
        else:
            return None

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, n: int):
        self._line_number = int(n)

    @property
    def line(self):
        return self._get_line(self.line_number)

    def _get_line(self, line_number: int):
        return getline(str(self.filename), int(line_number)).strip()

    def _next_line(self):
        self.line_number += 1

    def read_file(self):
        while self.line_number <= self.n_lines:
            if len(self.dataframes) == self.n_data_blocks:
                break

            elif self.line.startswith('data_'):
                self._read_data_block()

            if not self.line.startswith('data_'):
                self._next_line()

        self._to_numeric()
        return

    def _read_data_block(self):
        # Get dataframes block name and initialise empty list to store dataframes block
        self._current_data_block_name = self.line[5:]
        data_block = []

        # iterate over lines in each block and process as keywords are reached
        while self.line_number <= self.n_lines:
            self._next_line()

            if self.line.startswith('loop_'):
                self._read_loop_block()
                return

            elif self.line.startswith('data_') or self.line_number == self.n_lines:
                self._simple_data_block_to_dataframe(data_block)
                return

            data_block.append(self.line)
        return

    def _read_loop_block(self):
        self._next_line()
        header = self._read_loop_header()
        df = self._read_loop_data()
        df.columns = header
        df.name = self._current_data_block_name
        self.dataframes.append(df)
        return

    def _read_loop_header(self) -> List:
        loop_header = []

        while self.line.startswith('_'):
            heading = self.line.split()[0][1:]
            loop_header.append(heading)
            self._next_line()

        return loop_header

    def _read_loop_data(self) -> pd.DataFrame:
        buffer = """"""
        while self.line_number <= self.n_lines:
            if self.line.startswith('data_'):
                break
            buffer += self.line + '\n'
            self._next_line()

        df = pd.read_csv(StringIO(buffer), delim_whitespace=True, header=None, comment='#')
        return df

    def _simple_data_block_to_dataframe(self, data_block):
        data_clean = {}
        for line in data_block:
            if line == '' or line.startswith('#'):
                continue

            key = line.split()[0][1:]
            value = line.split()[1]
            data_clean[key] = value

        df = pd.DataFrame(data_clean, index=['value'])
        df.name = self._current_data_block_name
        self._add_dataframe(df)
        return

    def to_excel(self, filename: str):
        # Sanitise filename
        if not str(filename).endswith('.xlsx'):
            filename += '.xlsx'

        # Initialise sheet naming
        used_sheet_names = []
        sheet_index = 1

        iterable_df = self.dataframes

        with pd.ExcelWriter(filename) as writer:
            for df in iterable_df:
                df_name = getattr(df, 'name', None)

                # Set sheet name
                if df_name in (None, '') or df_name in used_sheet_names:
                    sheet_name = f'sheet{sheet_index}'
                    sheet_index += 1
                else:
                    sheet_name = df_name

                # Transpose 1 row dataframes for cleanness
                if df.shape[0] == 1:
                    df = df.transpose()

                # Write df into sheet
                df.to_excel(writer, sheet_name=sheet_name)
                used_sheet_names.append(sheet_name)

        return

    def _to_numeric(self):
        for idx, df in enumerate(self.dataframes):
            # applying pd.to_numeric loses name dataframes of DataFrame, need to extract and reapply here
            name = getattr(df, 'name', None)

            # to numeric
            self.dataframes[idx] = df.apply(pd.to_numeric, errors='ignore')

            # reapply name
            if name is not None:
                self.dataframes[idx].name = name

    def write_star_file(self, filename: str = None, **kwargs):
        # Set filename
        if filename is None:
            filename = self.filename

        # Write header
        with open(filename, 'w') as file:
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            file.write(f'# Created by the starfile python package (version {__version__}) on {now}\n')
        self._write_blank_lines(filename, 1)

        # Write each dataframes block
        for df in self.dataframes:
            self._write_data_block(df, filename, **kwargs)

        # Write newline at end of file
        self._write_blank_lines(filename, 1)
        return

    def _write_loopheader(self, dataframe: pd.DataFrame, filename: str) -> List:
        loopheader = ['loop_']
        headings = [f'_{column_name} #{idx}' for idx, column_name in enumerate(dataframe.columns, 1)]
        loopheader += headings

        with open(filename, 'a') as file:
            for line in loopheader:
                file.write(f'{line}\n')
        return

    def _write_data_block(self, dataframe: pd.DataFrame, filename: str, **kwargs):
        data_block_name = 'data_' + getattr(dataframe, 'name', '')

        with open(filename, 'a') as file:
            file.write(f'{data_block_name}\n\n')

        if dataframe.shape[0] == 1:
            self._write_data_block_simple(dataframe, filename)
        elif dataframe.shape[0] > 1:
            self._write_data_block_loop(dataframe, filename, **kwargs)
        else:
            raise ValueError('DataFrame does not have at least 1 row')
        self._write_blank_lines(filename, 2)
        return

    def _write_data_block_simple(self, dataframe: pd.DataFrame, filename: str):
        entries = [f'_{column_name}\t\t\t{dataframe[column_name][0]}' for column_name in dataframe.columns]

        with open(filename, 'a') as file:
            for entry in entries:
                file.write(f'{entry}\n')
        return

    def _write_blank_lines(self, filename: str, n: int):
        with open(filename, 'a') as file:
            for i in range(n):
                file.write('\n')
        return

    def _write_data_block_loop(self, dataframe: pd.DataFrame, filename: str, **kwargs):
        self._write_loopheader(dataframe, filename)

        # new main block
        if 'float_format' not in kwargs.keys():
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, float_format='%.8f', **kwargs)
        else:
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, **kwargs)
        return















