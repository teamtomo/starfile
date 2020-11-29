import datetime
from .version import __version__

class StarWriter:
    def __init__(self):
    def write_star_file(self, filename: str = None, **kwargs):
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







