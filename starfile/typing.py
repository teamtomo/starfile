from __future__ import annotations

from typing import Union, Dict
from typing_extensions import TypeAlias

import pandas as pd

DataBlock: TypeAlias = Union[
    pd.DataFrame,
    Dict[str, Union[str, int, float]]
]
