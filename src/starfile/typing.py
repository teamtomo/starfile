"""Type definitions for STAR file format."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

DataBlock: TypeAlias = pd.DataFrame | dict[str, str | int | float]
