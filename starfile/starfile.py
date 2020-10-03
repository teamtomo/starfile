from linecache import getline

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Union

from .version import __version__


class StarFile:
    def __init__(self, filename: str = None, data: Union[pd.DataFrame, List[pd.DataFrame]] = None):
        self.filename = filename
        self.dataframes = []

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
        if filename is not None:
            self._filename = Path(filename)
        else:
            self._filename = Path('starfile_auto.star')
        return

    @property
    def dataframes(self):
        if len(self._dataframes) == 1 and isinstance(self._dataframes, list):
            return self._dataframes[0]
        return self._dataframes

    @dataframes.setter
    def dataframes(self, dataframes: List[pd.DataFrame]):
        self._dataframes = dataframes

    @property
    def n_lines(self):
        if self.filename.exists():

            with open(self.filename, 'r') as f:
                n = sum(1 for line in f)
            return n

        else:
            return None

    @property
    def data_block_starts(self):
        """
        Return a list of indices in which line.strip() == 'data_'
        :return:
        """
        data_block_starts = []
        with open(self.filename) as file:
            for idx, line in enumerate(file, 1):
                if line.strip().startswith('data_'):
                    data_block_starts.append(idx)

        if len(data_block_starts) == 0:
            raise ValueError(f"File with name '{self.filename}' has no valid STAR data blocks")
        return data_block_starts

    @property
    def n_data_blocks(self):
        """
        Count the number of data blocks in the file
        :return:
        """
        n_data_blocks = len(self.data_block_starts)
        return n_data_blocks

    def _read_file(self):
        n_lines = self.n_lines
        data_block_starts = self.data_block_starts
        starts_ends = self._starts_ends(data_block_starts, n_lines)
        dataframes = []

        for data_block_start, data_block_end in starts_ends:
            df = self._read_data_block(data_block_start, data_block_end)
            dataframes.append(df)

        self.dataframes = dataframes

    def _read_data_block(self, data_block_start: int, data_block_end: int):
        line_number = data_block_start
        current_line = self._get_line(line_number)

        if not current_line.startswith('data_'):
            raise ValueError(f'Cannot start reading loop from line which does not indicate start of data block')

        data_block_name = current_line[5:]

        data_block = []
        line_number += 1

        # iterate over lines in each block and process as keywords are reached
        for line_number in range(line_number, data_block_end):
            current_line = self._get_line(line_number)

            if current_line.startswith('loop_'):
                data_block = self._read_loop_block(line_number, data_block_end)
                data_block.name = data_block_name
                return data_block

            elif current_line.startswith('#'):
                continue

            else:
                data_block.append(current_line)

        data_block = self._data_block_clean(data_block, data_block_name)
        return data_block

    def _read_loop_block(self, start_line_number: int, end_line_number: int):
        # read header
        header, data_block_start = self._read_loop_header(start_line_number)

        # get true data block endpoint
        #end_line_number = self._true_data_block_end(end_line_number)

        # read loop data into DataFrame
        df = self._read_loop_data(data_block_start, end_line_number)

        # Apply headings
        df.columns = header
        return df

    def _read_loop_data(self, start_line_number: int, end_line_number: int = None) -> pd.DataFrame:
        # Set amount of file to ignore before datablock
        header_length = start_line_number - 1
        true_end_line_number = self._true_data_block_end(end_line_number)

        # Read data blocks with pandas
        if end_line_number is None:
            df = pd.read_csv(self.filename, skiprows=header_length, delim_whitespace=True, header=None, comment='#')

        # workaround single line python engine problems
        elif true_end_line_number - start_line_number == 1:
            df = self._read_loop_data_single_line_python_engine(start_line_number, end_line_number)

        # case where footer is skipped
        else:
            footer_length = self.n_lines - end_line_number
            df = pd.read_csv(self.filename, skiprows=header_length, skipfooter=footer_length, delim_whitespace=True,
                             engine='python', header=None, comment='#')

        return df

    def _read_loop_data_single_line_python_engine(self, start_line_number: int, end_line_number: int) -> pd.DataFrame:
        """
        workaround to avoid problems with reading single line loop blocks with the python engine of pandas.read_csv()
        """
        header_length = start_line_number - 1
        footer_length = self.n_lines - end_line_number
        data = pd.read_csv(self.filename, skiprows=header_length, skipfooter=footer_length, delim_whitespace=True,
                             engine='python', header=0, comment='#').columns
        df = pd.DataFrame(data).T
        return df

    def _read_loop_header(self, start_line_number: int) -> Tuple[list, int]:
        """

        :param start_line_number: line number (1-indexed) with loop_ entry
        :return:
        """
        loop_header = []
        line_number = start_line_number

        # Check that loop header starts with loop
        line = getline(str(self.filename), line_number).strip()
        if not line.startswith('loop_'):
            raise ValueError(f'Cannot start reading loop from line which does not indicate start of loop block')

        # Advance then iterate over lines while in loop header
        line_number +=1
        line = self._get_line(line_number)

        while line.startswith('_'):
            if line.startswith('_'):
                line = line.split()[0][1:]  # Removes leading '_' and numbers in loopheader if present
                loop_header.append(line)
                line_number += 1
            line = self._get_line(line_number)

        data_block_start = line_number
        return loop_header, data_block_start

    def _get_line(self, line_number: int):
        return getline(str(self.filename), line_number).strip()

    def _starts_ends(self, data_block_starts, n_lines):
        """
        tuple of start and end line numbers
        :return:
        """
        starts_ends = [(start, end - 1) for start, end in zip(data_block_starts, data_block_starts[1:])]
        starts_ends.append((data_block_starts[-1], n_lines))
        return starts_ends

    def _data_block_clean(self, data_block, data_block_name):
        """
        Make a pandas dataframe from the names and info in a data block from a star file in a list of lists
        :param data_block:
        :return:
        """
        data_clean = {}
        for line in data_block:

            if line == '':
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
        iterable_df = self.iterable_dataframes
        for idx, df in enumerate(iterable_df):
            name = getattr(df, 'name', None)
            iterable_df[idx] = df.apply(pd.to_numeric, errors='ignore')
            if name is not None:
                iterable_df[idx].name = name
        self.dataframes = iterable_df

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
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, float_format='%.5f', **kwargs)
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
        current_line = self._get_line(current_line_number)

        # step back over lines until you reach the true end of the data block
        while current_line == "" or current_line.startswith('#'):
            current_line_number -= 1
            current_line = self._get_line(current_line_number)

        # return new data block end
        new_data_block_end = current_line_number + 1
        return new_data_block_end












