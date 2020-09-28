from typing import Union, List

import pandas as pd

from .starfile import StarFile
from .version import __version__


def open(filename: str) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename: file from which to read data
    :return:
    """
    df = StarFile(filename).dataframes
    return df


def read(filename: str) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename: file from which to read data
    :return:
    """
    df = open(filename)
    return df


def new(data: Union[pd.DataFrame, List[pd.DataFrame]], filename: str, **kwargs):
    """
    Write data from pandas dataframe(s) to a star file
    :param data: data in pandas dataframe(s) to be written to file
    :param filename: filename in which to new data
    :return:
    """
    star = StarFile(data=data)
    star.write_star_file(filename, **kwargs)
    return


def write(data: Union[pd.DataFrame, List[pd.DataFrame]], filename: str):
    """
    Write data from pandas dataframe(s) to a star file
    :param data: data in pandas dataframe(s) to be written to file
    :param filename: filename in which to new data
    :return:
    """
    star = StarFile(data=data)
    star.write_star_file(filename)
    return


def star2excel(star_file: str, excel_filename: str):
    """
    Converts a star file to an excel (.xlsx) file
    :param star_file: STAR file
    :param excel_filename: filename (should end in '.xlsx')
    :return:
    """
    star = StarFile(star_file)
    star.to_excel(excel_filename)
    return


def version():
    """
    Returns the current version of starfile
    :return:
    """
    return __version__
