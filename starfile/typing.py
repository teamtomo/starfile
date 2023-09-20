from __future__ import annotations

from typing import TypeAlias, Union, Dict

import pandas as pd

DataBlock: TypeAlias = Union[
    pd.DataFrame,
    Dict[str, Union[str, int, float]]
]
