from linecache import getline
from io import StringIO
from itertools import chain
from typing import Tuple, List, Union
from functools import cached_property

import pandas as pd
from datetime import datetime
from pathlib import Path


from .version import __version__


class StarFile:
    def __init__(self, filename: str = 'test.star',
                 data: Union[pd.DataFrame, List[pd.DataFrame]] = None,
                 max_data_blocks: int = None):
        self.filename = filename
        self.dataframes = []
        self.max_data_blocks = max_data_blocks
        self._line_number = 1
        self.line = ''

        if self.filename.exists():
            self._read_file()

        if isinstance(data, pd.DataFrame) or isinstance(data, list):
            self._append_data(data)

        self._to_numeric()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = Path(filename)

    @cached_property
    def n_lines(self):
        """
        count number of lines in file
        :return:
        """
        with open(self.filename, 'rb') as f:
            lines = 0
            buffer_size = 1024 * 1024
            buffer = f.read(buffer_size)
            while buffer:
                lines += buffer.count(b'\n')
                buffer = f.read(buffer_size)
            return lines

    @property
    def dataframes(self):
        if len(self._dataframes) == 1 and isinstance(self._dataframes, list):
            return self._dataframes[0]
        return self._dataframes

    @dataframes.setter
    def dataframes(self, dataframes: List[pd.DataFrame]):
        self._dataframes = dataframes

    def _read_file(self):
        dataframes = []
        with open(self.filename, 'r') as star_file:
            while self._line_number <= self.n_lines + 1:
                if self.line.startswith('data_'):
                    dataframes.append(self._read_data_block())

                # don't read more of the file if the max number of dataframes has been reached
                if len(dataframes) == self.max_data_blocks:
                    break
                self._next_line()

        self.dataframes = dataframes

    def _read_data_block(self):
        # Get data block name and initialise data block
        data_block_name = self.line[5:]
        data_block = []

        # iterate over lines in each block and process as keywords are reached
        while self._line_number <= self.n_lines + 1:
            if self.line.startswith('data_'):
                break

            elif self.line.startswith('loop_'):
                df = self._read_loop_block()
                df.name = data_block_name
                return df
            self._next_line()
            data_block.append(self.line)


        data_block = self._clean_simple_data_block(data_block, data_block_name)
        return data_block

    def _read_loop_block(self):
        # read header
        header = self._read_loop_header()

        # read loop data into DataFrame
        df = self._read_loop_data()

        # Apply headings
        df.columns = header
        return df

    def _read_loop_data(self) -> pd.DataFrame:
        # Initialise loop data, line and line number
        loop_data = """"""

        while self._line_number <= self.n_lines + 1:
            if self.line.startswith('data_'):
                break
            loop_data += self.line + '\n'
            self._next_line()

        df = pd.read_csv(StringIO(loop_data), delim_whitespace=True, header=None, comment='#')
        return df

    def _read_loop_header(self) -> list:
        # Initialise loop header, line number and line
        loop_header = []
        self._next_line()

        while self.line.startswith('_') or self.line.startswith('loop_'):
            if self.line.startswith('_'):
                line = self.line.split()[0][1:]  # Removes leading '_' and numbers in loopheader if present
                loop_header.append(line)
            self._next_line()

        return loop_header

    def _next_line(self):
        self._line = getline(str(self.filename), self._line_number).strip()
        self._line_number += 1

    @property
    def line(self):
        return self._line

    def _clean_simple_data_block(self, data_block, data_block_name):
        """
        Make a pandas dataframe from the names and info in a data block from a star file in a list of lists
        :param data_block:
        :return:
        """
        data_clean = {}
        for line in data_block:

            if line == '' or line.startswith('#'):
                continue

            name_and_data = line.split()
            key = name_and_data[0][1:]
            value = name_and_data[1]

            data_clean[key] = value

        df = pd.DataFrame(data_clean, index=['value'])
        df.name = data_block_name
        return df

    def to_excel(self, filename: str):
        # Sanitise filename
        if not str(filename).endswith('.xlsx'):
            filename += '.xlsx'

        # Initialise sheet naming
        used_sheet_names = []
        sheet_index = 1

        iterable_df = self.iterable_dataframes

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

    @property
    def iterable_dataframes(self):
        if isinstance(self.dataframes, pd.DataFrame):
            iterable_df = [self.dataframes]
        else:
            iterable_df = self.dataframes
        return iterable_df

    def _to_numeric(self):
        for idx, df in enumerate(self.iterable_dataframes):
            # applying pd.to_numeric loses name data of DataFrame, need to extract and reapply here
            name = getattr(df, 'name', None)

            # to numeric
            self.iterable_dataframes[idx] = df.apply(pd.to_numeric, errors='ignore')

            # reapply name
            if name is not None:
                self.iterable_dataframes[idx].name = name
        self.dataframes = self.iterable_dataframes

    def write_star_file(self, filename: str = None, **kwargs):
        # Set filename
        if filename is None:
            filename = self.filename

        # Write header
        with open(filename, 'w') as file:
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            file.write(f'# Created by the starfile python package (version {__version__}) on {now}\n')
        self._write_blank_lines(filename, 1)

        # Write each data block
        for df in self.iterable_dataframes:
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
        # new loopheader
        self._write_loopheader(dataframe, filename)

        # new main block
        if 'float_format' not in kwargs.keys():
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, float_format='%.8f', **kwargs)
        else:
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, **kwargs)
        return

    def _append_data(self, data: pd.DataFrame):
        self.dataframes = self.iterable_dataframes
        if isinstance(data, pd.DataFrame):
            data = [data]
        self.dataframes += data
        return

    def _true_data_block_end(self, data_block_end: int) -> int:
        """
        trims unnecessary info from end of data block to ensure correct parsing when passed to pandas
        """
        current_line_number = data_block_end
        current_line = self._next_line(current_line_number)

        # step back over lines until you reach the true end of the data block
        while current_line == "" or current_line.startswith('#'):
            current_line_number -= 1
            current_line = self._next_line(current_line_number)

        # return new data block end
        new_data_block_end = current_line_number + 1
        return new_data_block_end

    @line.setter
    def line(self, line):
        self._line = line











