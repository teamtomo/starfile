"""STAR file IO in Python."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("starfile")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Alister Burt"
__email__ = "alisterburt@gmail.com"

from starfile.functions import read, write

__all__ = [
    "read",
    "write",
]
