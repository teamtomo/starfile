from typing import Union, List

import pandas as pd

from .starfile import StarFile


def read(filename: str) -> Union[pd.DataFrame, List[pd.DataFrame]]:
    """
    Read a star file into a pandas dataframe or list of pandas dataframes
    :param filename:
    :return:
    """
    df = StarFile(filename).dataframes
    return df

