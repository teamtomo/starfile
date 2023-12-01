from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike

from .parser import StarParser
from .writer import StarWriter
from .typing import DataBlock

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike


def read(filename: PathLike, read_n_blocks: int = None, always_dict: bool = False, quotechar: str = '"'):
    """
    Read a star file into a pandas dataframe or dict of pandas dataframes

    default behaviour in the case of only one data block being present in the STAR file is to
    return only a dataframe, this can be changed by setting 'always_dict=True'

    The quote character that is optional for strings in the star file can be changed by setting
    'quotechar' to the desired character
    """

    parser = StarParser(filename, n_blocks_to_read=read_n_blocks, quotechar=quotechar)
    if len(parser.data_blocks) == 1 and always_dict is False:
        return list(parser.data_blocks.values())[0]
    else:
        return parser.data_blocks


def write(
    data: Union[DataBlock, Dict[str, DataBlock], List[DataBlock]],
    filename: PathLike,
    float_format: str = '%.6f',
    sep: str = '\t',
    na_rep: str = '<NA>',
    **kwargs,
):
    """Write data blocks as STAR files."""
    StarWriter(
        data,
        filename=filename,
        float_format=float_format,
        na_rep=na_rep,
        separator=sep
    )
