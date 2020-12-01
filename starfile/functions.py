from typing import Dict, List, Union

import pandas as pd

from .parser import StarParser
from .writer import StarWriter


def open(filename: str, read_n_blocks: int = None, always_dict: bool = False):
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


def read(filename: str, read_n_blocks: int = None, always_dict: bool = False):
    """
    Read a star file into a pandas dataframe or dict of pandas dataframes

    default behaviour in the case of only one data block being present in the STAR file is to
    return only a dataframe, this can be changed by setting 'always_dict=True'
    """
    return open(filename, read_n_blocks=read_n_blocks, always_dict=always_dict)


def new(data: Union[pd.DataFrame, Dict[str, pd.DataFrame], List[pd.DataFrame]], filename: str,
        float_format: str = '%.6f', overwrite: bool = False):
    """
    Write dataframes from pandas dataframe(s) to a star file

    data can be a single dataframe, a list of dataframes or a dict of dataframes
    float format defaults to 6 digits after the decimal point
    """
    StarWriter(data, filename=filename, float_format=float_format, overwrite=overwrite)
    return


def write(data: Union[pd.DataFrame, Dict[str, pd.DataFrame], List[pd.DataFrame]], filename: str,
          float_format: str = '%.6f', overwrite: bool = False):
    """
    Write dataframes from pandas dataframe(s) to a star file

    data can be a single dataframe, a list of dataframes or a dict of dataframes
    float format defaults to 6 digits after the decimal point
    """
    new(data, filename=filename, float_format=float_format, overwrite=overwrite)
