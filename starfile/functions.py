from typing import Union, List
from pathlib import Path

import pandas as pd

from .parser import StarParser
from .version import __version__

def open(filename: str, n_data_blocks: int = None) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename: file from which to read dataframes
    :return:
    """
    if Path(filename).exists():
        return StarParser(filename, read_n_blocks=n_data_blocks).data
    else:
        raise FileNotFoundError


def read(filename: str, n_data_blocks: int = None) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename: file from which to read dataframes
    :return:
    """
    df = open(filename, n_data_blocks)
    return df


def new(data: Union[pd.DataFrame, List[pd.DataFrame]], filename: str, **kwargs):
    """
    Write dataframes from pandas dataframe(s) to a star file
    :param data: dataframes in pandas dataframe(s) to be written to file
    :param filename: filename in which to new dataframes
    :return:
    """
    star = StarParser(data=data)
    star.write_star_file(filename, **kwargs)
    return


def write(data: Union[pd.DataFrame, List[pd.DataFrame]], filename: str):
    """
    Write dataframes from pandas dataframe(s) to a star file
    :param data: dataframes in pandas dataframe(s) to be written to file
    :param filename: filename in which to new dataframes
    :return:
    """
    star = StarParser(data=data)
    star.write_star_file(filename)
    return


def star2excel(star_file: str, excel_filename: str):
    """
    Converts a star file to an excel (.xlsx) file
    :param star_file: STAR file
    :param excel_filename: filename (should end in '.xlsx')
    :return:
    """
    star = StarParser(star_file)
    star.to_excel(excel_filename)
    return


def version():
    """
    Returns the current version of starfile
    :return:
    """
    return __version__
