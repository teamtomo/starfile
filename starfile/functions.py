from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike

from .parser import StarParser
from .writer import StarWriter

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike


def read(filename: PathLike, read_n_blocks: int = None, always_dict: bool = False):
    """
    Read a star file into a pandas dataframe or dict of pandas dataframes

    default behaviour in the case of only one data block being present in the STAR file is to
    return only a dataframe, this can be changed by setting 'always_dict=True'
    """
    star = StarParser(filename, read_n_blocks=read_n_blocks)
    if len(star.dataframes) == 1 and always_dict is False:
        return star.first_dataframe
    else:
        return star.dataframes


def write(data: Union[pd.DataFrame, Dict[str, pd.DataFrame], List[pd.DataFrame]],
          filename: PathLike,
          float_format: str = '%.6f', sep: str = '\t', na_rep: str = '<NA>',
          overwrite: bool = False):
    """
    Write dataframes from pandas dataframe(s) to a star file

    data can be a single dataframe, a list of dataframes or a dict of dataframes
    float format defaults to 6 digits after the decimal point
    """
    StarWriter(data, filename=filename, float_format=float_format, overwrite=overwrite)
