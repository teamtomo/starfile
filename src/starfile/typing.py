from __future__ import annotations

from typing import Dict, Union

import pandas as pd
from typing_extensions import TypeAlias

DataBlock: TypeAlias = Union[pd.DataFrame, Dict[str, Union[str, int, float]]]
