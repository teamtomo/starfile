from typing import Union, List

import pandas as pd

from .starfile import StarFile
from .version import VERSION


def read(filename: str) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename:
    :return:
    """
    df = StarFile(filename).dataframes
    return df


def write(data: Union[pd.DataFrame, List[pd.DataFrame]], filename: str):
    """
    Write data from pandas dataframe(s) to a star file
    :param data: data in pandas dataframe(s) to be written to file
    :param filename: filename in which to write data
    :return:
    """
    star = StarFile(data=data)
    star.write_star_file(filename)
    return


def version():
    """
    Returns the current version of starfile
    :return:
    """
    return VERSION
