from __future__ import annotations

from typing import TYPE_CHECKING

from .parser import StarParser
from .typing import DataBlock
from .writer import StarWriter

if TYPE_CHECKING:
    from os import PathLike


def read(filename: PathLike, read_n_blocks: int = None, always_dict: bool = False):
    """Read a STAR file.

    Default behaviour in the case of only one data block being present in the STAR file
    is to return only a dataframe, this can be changed by setting 'always_dict=True'
    """
    parser = StarParser(filename, n_blocks_to_read=read_n_blocks)
    if len(parser.data_blocks) == 1 and always_dict is False:
        return list(parser.data_blocks.values())[0]
    else:
        return parser.data_blocks


def write(
    data: DataBlock | dict[str, DataBlock] | list[DataBlock],
    filename: PathLike,
    float_format: str = "%.6f",
    sep: str = "\t",
    na_rep: str = "<NA>",
    **kwargs,
):
    """Write data blocks as STAR files."""
    StarWriter(
        data, filename=filename, float_format=float_format, na_rep=na_rep, separator=sep
    )
