from __future__ import annotations

from typing import Dict, Union

import pandas as pd
import polars as pl
from typing_extensions import TypeAlias

DataBlock: TypeAlias = Union[
    pd.DataFrame | pl.DataFrame, Dict[str, Union[str, int, float]]
]
