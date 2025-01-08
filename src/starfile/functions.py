from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike

from .parser import StarParser
from .writer import StarWriter
from .typing import DataBlock

if TYPE_CHECKING:
    import pandas as pd
    from os import PathLike


def read(
    filename: PathLike,
    read_n_blocks: Optional[int] = None,
    always_dict: bool = False,
    parse_as_string: List[str] = []
) -> Union[DataBlock, Dict[DataBlock]]:
    """Read data from a STAR file.

    Basic data blocks are read as dictionaries. Loop blocks are read as pandas
    dataframes. When multiple data blocks are present a dictionary of datablocks is
    returned. When a single datablock is present only the block is returned by default.
    To force returning a dectionary even when only one datablock is present set
    `always_dict=True`.

    Parameters
    ----------
    filename: PathLike
        File from which to read data.
    read_n_blocks: int | None
        Limit reading the file to the first n data blocks.
    always_dict: bool
        Always return a dictionary, even when only a single data block is present.
    parse_as_string: list[str]
        A list of keys or column names which will not be coerced to numeric values.
    """
    parser = StarParser(filename, n_blocks_to_read=read_n_blocks, parse_as_string=parse_as_string)
    if len(parser.data_blocks) == 1 and always_dict is False:
        return list(parser.data_blocks.values())[0]
    else:
        return parser.data_blocks


def write(
    data: Union[DataBlock, Dict[str, DataBlock], List[DataBlock]],
    filename: PathLike,
    float_format: str = '%.6f',
    sep: str = '\t',
    na_rep: str = '<NA>',
    quote_character: str = '"',
    quote_all_strings: bool = False,
    **kwargs
):
    """Write data to disk in the STAR format.

    Parameters
    ----------
    data: DataBlock | Dict[str, DataBlock] | List[DataBlock]
        Data to be saved to file. DataBlocks are dictionaries or dataframes.
        If a dictionary of datablocks are passed the keys will be the data block names.
    filename: PathLike
        Path where the file will be saved.
    float_format: str
        Float format string which will be passed to pandas.
    sep: str
        Separator between values, will be passed to pandas.
    na_rep: str
        Representation of null values, will be passed to pandas.
    """
    StarWriter(
        data,
        filename=filename,
        float_format=float_format,
        na_rep=na_rep,
        separator=sep,
        quote_character=quote_character,
        quote_all_strings=quote_all_strings,
    ).write()


def to_string(
    data: Union[DataBlock, Dict[str, DataBlock], List[DataBlock]],
    float_format: str = '%.6f',
    sep: str = '\t',
    na_rep: str = '<NA>',
    quote_character: str = '"',
    quote_all_strings: bool = False,
    **kwargs
):
    """Represent data in the STAR format.

    Parameters
    ----------
    data: DataBlock | Dict[str, DataBlock] | List[DataBlock]
        Data to represent. DataBlocks are dictionaries or dataframes.
        If a dictionary of datablocks are passed the keys will be the data block names.
    float_format: str
        Float format string which will be passed to pandas.
    sep: str
        Separator between values, will be passed to pandas.
    na_rep: str
        Representation of null values, will be passed to pandas.
    """
    writer = StarWriter(
        data,
        filename=None,
        float_format=float_format,
        na_rep=na_rep,
        separator=sep,
        quote_character=quote_character,
        quote_all_strings=quote_all_strings,
    )
    return writer.to_string()
