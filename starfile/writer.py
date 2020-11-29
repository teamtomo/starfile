import datetime
from typing import Union
from pathlib import Path
from .version import __version__


class StarWriter:
    def __init__(self, filename: Union[Path, str]):
        self.filename = filename

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

    def add_package_info_to_buffer(self):
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        line = f'Created by the starfile Python package (version {__version__}) on {now}\n'
        self.add_comment_to_buffer(line)


    def write_star_file(self, filename: str = None, **kwargs):
        self.add_package_info_to_buffer()
        self.add_blank_line_to_buffer()

        for _, df in self.dataframes.items():
            self._write_data_block(df, filename, **kwargs)

        self.add_blank_line_to_buffer()
        return

    def _write_loopheader(self, dataframe: pd.DataFrame, filename: str) -> List:
        loopheader = ['loop_']
        headings = [f'_{column_name} #{idx}' for idx, column_name in
                    enumerate(dataframe.columns, 1)]
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

    def _write_data_block_loop(self, dataframe: pd.DataFrame, filename: str, **kwargs):
        self._write_loopheader(dataframe, filename)

        # new main block
        if 'float_format' not in kwargs.keys():
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False,
                             float_format='%.8f', **kwargs)
        else:
            dataframe.to_csv(filename, mode='a', sep='\t', header=False, index=False, **kwargs)
        return
