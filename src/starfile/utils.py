"""Utility classes for text buffer and file handling."""
from __future__ import annotations

from collections import deque
from linecache import checkcache, getline
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike


class TextBuffer:
    """Buffer for accumulating text lines."""

    def __init__(self) -> None:
        """Initialize text buffer."""
        self.buffer: deque[str] = deque()

    @property
    def is_empty(self) -> bool:
        """Check if buffer is empty or contains only whitespace."""
        if len(self.buffer) == 0:
            return True
        elif len(self.buffer) <= 100:  # arbitrary, avoid iterating large buffer
            return all(item.strip() == "" for item in self.buffer)
        return False

    def clear(self) -> None:
        """Clear the buffer."""
        self.buffer = deque()

    def add_line(self, line: str) -> None:
        """Add a line to the buffer."""
        self.buffer.append(f"{line}")

    def add_comment(self, line: str) -> None:
        """Add a comment line to the buffer."""
        self.add_line(f"# {line}")

    def add_blank_line(self) -> None:
        """Add a blank line to the buffer."""
        self.add_line("")

    def add_blank_lines(self, n: int) -> None:
        """Add n blank lines to the buffer."""
        for _ in range(n):
            self.add_blank_line()

    def as_str(self) -> str:
        """Return buffer contents as a string."""
        buffer_with_newlines = "\n".join(self.buffer)
        if buffer_with_newlines[-2:] != "\n":
            buffer_with_newlines = f"{buffer_with_newlines}\n"
        return buffer_with_newlines

    def write_to_disk(self, filename: PathLike, mode: str) -> None:
        """Write buffer contents to disk."""
        with open(filename, mode) as file:
            file.write(self.as_str())

    def write_as_new_file(self, filename: PathLike) -> None:
        """Write buffer as new file."""
        self.write_to_disk(filename, "w+")

    def write_as_new_file_and_clear(self, filename: PathLike) -> None:
        """Write buffer as new file and clear it."""
        self.write_as_new_file(filename)
        self.clear()

    def append_to_file(self, filename: PathLike) -> None:
        """Append buffer contents to existing file."""
        self.write_to_disk(filename, "a")

    def append_to_file_and_clear(self, filename: PathLike) -> None:
        """Append buffer to file and clear it."""
        self.append_to_file(filename)
        self.clear()


class TextCrawler:
    """Crawler for reading lines from a file."""

    def __init__(self, filename: PathLike) -> None:
        """Initialize text crawler."""
        self.filename = filename
        self._current_line_number = 0
        checkcache(str(self.filename))

    def count_lines(self) -> int:
        """Count lines in file."""
        with open(self.filename, "rb") as f:
            return sum(1 for _ in f)

    @property
    def current_line_number(self) -> int:
        """Get current line number."""
        return self._current_line_number

    @current_line_number.setter
    def current_line_number(self, n: int) -> None:
        """Set current line number."""
        self._current_line_number = n

    @property
    def current_line(self) -> str:
        """Get current line from file."""
        return self.get_line(self.current_line_number)

    def get_line(self, line_number: int) -> str:
        """Get a specific line from file."""
        return getline(str(self.filename), line_number).strip()

    def increment_line_number(self) -> None:
        """Increment current line number."""
        self._current_line_number += 1
