import numpy as np
import pandas as pd

import starfile
from .constants import test_data_directory

million_row_file = test_data_directory / '1m_row.star'


def generate_large_star_file():
    df = pd.DataFrame(np.random.randint(0, 100, size=(100000, 4)), columns=list('ABCD'))
    starfile.write(df, million_row_file, overwrite=True)


def remove_large_star_file():
    million_row_file.unlink()
