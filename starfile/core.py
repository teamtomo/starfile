from pathlib import Path
from linecache import getline
from typing import Union


class TextBuffer:
    def __init__(self):
        self.buffer = ''

    def clear(self):
        self.buffer = ''

    def add_newline(self):
        self.buffer += '\n'

    def add_line(self, line):
        self.buffer += f'{line}'
        self.add_newline()

    def add_comment(self, line):
        self.add_line(f'# {line}')

    def add_blank_line(self):
        self.add_newline()

    def add_blank_lines(self, n: int):
        for i in range(n):
            self.add_blank_line()

    def write_to_disk(self, filename: Union[Path, str], mode: str):
        with open(filename, mode) as file:
            file.write(self.buffer)

    def write_as_new_file(self, filename: Union[Path, str]):
        self.write_to_disk(filename, 'w+')

    def write_as_new_file_and_clear(self, filename: Union[Path, str]):
        self.write_as_new_file(filename)
        self.clear()

    def append_to_file(self, filename: Union[Path, str]):
        self.write_to_disk(filename, 'a')

    def append_to_file_and_clear(self, filename: Union[Path, str]):
        self.append_to_file(filename)
        self.clear()

    def split_on_newline(self):
        return self.buffer.split('\n')[:-1]


class TextCrawler:
    def __init__(self, filename: Union[Path, str]):
        self.filename = filename
        self.current_line_number = 0

    def count_lines(self):
        with open(self.filename, 'rb') as f:
            return sum(1 for line in f)

    @property
    def current_line_number(self):
        return self._current_line_number

    @current_line_number.setter
    def current_line_number(self, n: int):
        self._current_line_number = n

    @property
    def current_line(self):
        return self.get_line(self.current_line_number)

    @current_line_number.setter
    def current_line_number(self, line_number: int):
        self._current_line_number = line_number

    def get_line(self, line_number: int):
        return getline(str(self.filename), line_number).strip()

    def increment_line_number(self):
        self._current_line_number += 1
