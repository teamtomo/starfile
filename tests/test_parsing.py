import time

import pandas as pd
import numpy as np
import pytest

from starfile.parser import StarParser
from .constants import (
    loop_simple,
    postprocess,
    pipeline,
    rln31_style,
    optimiser_2d,
    optimiser_3d,
    sampling_2d,
    sampling_3d,
    single_line_middle_of_multiblock,
    single_line_end_of_multiblock,
    non_existant_file,
    loop_simple_columns,
    two_single_line_loop_blocks,
    two_basic_blocks,
    empty_loop,
)
from .utils import generate_large_star_file, remove_large_star_file, million_row_file


def test_instantiation():
    """
    Tests instantiation of the StarFile class
    """
    # instantiation with file which exists
    s = StarParser(loop_simple)

    # instantiation with non-existant file should fail
    assert non_existant_file.exists() is False
    with pytest.raises(FileNotFoundError):
        s = StarParser(non_existant_file)


def test_read_loop_block():
    """
    Check that loop block is parsed correctly, data has the correct shape
    """
    s = StarParser(loop_simple)

    # Check the output
    for idx, key in enumerate(s.dataframes.keys()):
        # Check that only one object is present
        assert idx < 1

        # get dataframe
        df = s.dataframes[key]
        assert isinstance(df, pd.DataFrame)

        # Check shape of dataframe
        assert df.shape == (16, 12)

        # check columns
        assert all(df.columns == loop_simple_columns)


def test_read_multiblock_file():
    """
    Check that multiblock STAR files such as postprocess RELION files
    parse properly
    """
    s = StarParser(postprocess)
    assert len(s.dataframes) == 3

    for key, df in s.dataframes.items():
        assert isinstance(df, pd.DataFrame)

    assert s.dataframes['general'].shape == (1, 6)
    assert all(
        ['rlnFinalResolution', 'rlnBfactorUsedForSharpening', 'rlnUnfilteredMapHalf1',
         'rlnUnfilteredMapHalf2', 'rlnMaskName', 'rlnRandomiseFrom']
        == s.dataframes['general'].columns)
    assert s.dataframes['fsc'].shape == (49, 7)
    assert s.dataframes['guinier'].shape == (49, 3)


def test_read_pipeline():
    """
    Check that a pipeline.star file is parsed correctly
    """
    s = StarParser(pipeline)
    for key, df in s.dataframes.items():
        assert isinstance(df, pd.DataFrame)

    # Check that dataframes have the correct shapes
    assert s.dataframes['pipeline_general'].shape == (1, 1)
    assert s.dataframes['pipeline_processes'].shape == (31, 4)
    assert s.dataframes['pipeline_nodes'].shape == (74, 2)
    assert s.dataframes['pipeline_input_edges'].shape == (48, 2)
    assert s.dataframes['pipeline_output_edges'].shape == (72, 2)


def test_read_rln31():
    """
    Check that reading of RELION 3.1 style star files works properly
    """
    s = StarParser(rln31_style)

    for key, df in s.dataframes.items():
        assert isinstance(df, pd.DataFrame)

    assert isinstance(s.dataframes['block_1'], pd.DataFrame)
    assert isinstance(s.dataframes['block_2'], pd.DataFrame)
    assert isinstance(s.dataframes['block_3'], pd.DataFrame)


def test_read_n_blocks():
    """
    Check that passing read_n_blocks allows reading of only a specified
    number of data blocks from a star file
    """
    # test 1 block
    s = StarParser(postprocess, read_n_blocks=1)
    assert len(s.dataframes) == 1

    # test 2 blocks
    s = StarParser(postprocess, read_n_blocks=2)
    assert len(s.dataframes) == 2


def test_single_line_middle_of_multiblock():
    s = StarParser(single_line_middle_of_multiblock)
    assert len(s.dataframes) == 2


def test_single_line_end_of_multiblock():
    s = StarParser(single_line_end_of_multiblock)
    assert len(s.dataframes) == 2

    # iterate over dataframes, checking keys, names and shapes
    for idx, (key, df) in enumerate(s.dataframes.items()):
        assert df.name == 'block_3'
        if idx == 0:
            assert key == 'block_3'
            assert df.shape == (2, 5)
        if idx == 1:
            assert key == 1
            assert df.shape == (1, 5)


def test_read_optimiser_2d():
    s = StarParser(optimiser_2d)
    assert len(s.dataframes) == 1
    assert s.dataframes['optimiser_general'].shape == (1, 84)


def test_read_optimiser_3d():
    s = StarParser(optimiser_3d)
    assert len(s.dataframes) == 1
    assert s.dataframes['optimiser_general'].shape == (1, 84)


def test_read_sampling_2d():
    s = StarParser(sampling_2d)
    assert len(s.dataframes) == 1
    assert s.dataframes['sampling_general'].shape == (1, 12)


def test_read_sampling_3d():
    s = StarParser(sampling_3d)
    assert len(s.dataframes) == 2
    assert s.dataframes['sampling_general'].shape == (1, 15)
    assert s.dataframes['sampling_directions'].shape == (192, 2)


def test_df_as_list():
    s = StarParser(sampling_3d)
    assert isinstance(s.dataframes_as_list(), list)
    assert len(s.dataframes_as_list()) == 2


def test_first_dataframe():
    s = StarParser(sampling_3d)
    assert isinstance(s.first_dataframe, pd.DataFrame)


def test_parsing_speed():
    generate_large_star_file()
    start = time.time()
    s = StarParser(million_row_file)
    end = time.time()
    remove_large_star_file()

    # Check that execution takes less than a second
    assert end - start < 1


def test_two_single_line_loop_blocks():
    parser = StarParser(two_single_line_loop_blocks)
    assert len(parser.dataframes) == 2

    np.testing.assert_array_equal(
        parser.dataframes['block_0'].columns, [f'val{i}' for i in (1, 2, 3)]
    )
    assert parser.dataframes['block_0'].shape == (1, 3)

    np.testing.assert_array_equal(
        parser.dataframes['block_1'].columns, [f'col{i}' for i in (1, 2, 3)]
    )
    assert parser.dataframes['block_1'].shape == (1, 3)


def test_two_basic_blocks():
    parser = StarParser(two_basic_blocks)
    assert len(parser.dataframes) == 2
    for df in parser.dataframes.values():
        assert df.shape == (1, 3)


def test_empty_loop_block():
    """Parsing an empty loop block should return an empty dataframe."""
    parser = StarParser(empty_loop)
    assert len(parser.dataframes) == 1
