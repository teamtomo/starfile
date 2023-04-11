from __future__ import annotations

from collections import deque
from linecache import getline, checkcache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike


class TextBuffer:
    def __init__(self):
        self.buffer = deque()

    @property
    def is_empty(self) -> bool:
        if len(self.buffer) == 0:
            return True
        elif len(self.buffer) <= 100:  # arbitrary, avoid iterating large buffer
            return all([item.strip() == '' for item in self.buffer])
        else:
            return False

    def clear(self):
        self.buffer = deque()

    def add_line(self, line):
        self.buffer.append(f'{line}')

    def add_comment(self, line):
        self.add_line(f'# {line}')

    def add_blank_line(self):
        self.add_line('')

    def add_blank_lines(self, n: int):
        for i in range(n):
            self.add_blank_line()

    def as_str(self):
        buffer_with_newlines = '\n'.join(self.buffer)
        if buffer_with_newlines[-2:] != '\n':
            buffer_with_newlines = f'{buffer_with_newlines}\n'
        return buffer_with_newlines

    def write_to_disk(self, filename: PathLike, mode: str):
        with open(filename, mode) as file:
            file.write(self.as_str())

    def write_as_new_file(self, filename: PathLike):
        self.write_to_disk(filename, 'w+')

    def write_as_new_file_and_clear(self, filename: PathLike):
        self.write_as_new_file(filename)
        self.clear()

    def append_to_file(self, filename: PathLike):
        self.write_to_disk(filename, 'a')

    def append_to_file_and_clear(self, filename: PathLike):
        self.append_to_file(filename)
        self.clear()


class TextCrawler:
    def __init__(self, filename: PathLike):
        self.filename = filename
        self.current_line_number = 0
        checkcache(str(self.filename))

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
