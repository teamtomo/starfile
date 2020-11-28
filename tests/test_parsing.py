import pandas as pd
import pytest

from starfile.parser import StarParser
from .constants import loop_simple, postprocess, pipeline, rln31_style, optimiser_2d, optimiser_3d, sampling_2d, \
    sampling_3d, single_line_middle_of_multiblock, single_line_end_of_multiblock, non_existant_file, loop_simple_columns


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




def test_read_data_block_simple():
    """
    Check that simple data blocks (no loops) are read correctly
    """
    s = StarParser(postprocess)
    s.current_line_number = 4
    s._parse_data_block()
    assert isinstance(s.dataframes[-1], pd.DataFrame)
    assert s.dataframes[-1].shape == (1, 6)


def test_read_file_multiblock():
    """
    Check that multiblock STAR files such as postprocess RELION files
    parse properly
    """
    s = StarParser(postprocess)
    assert len(s.dataframes) == 3
    assert all([isinstance(s.dataframes[i], pd.DataFrame) for i in range(3)])
    assert s.dataframes[0].shape == (1, 6)
    assert s.dataframes[1].shape == (49, 7)
    assert s.dataframes[2].shape == (49, 3)


def test_read_pipeline():
    """
    Check that a pipeline.star file is parsed correctly
    """
    s = StarParser(pipeline)
    assert isinstance(s.dataframes, list)
    for i in range(5):
        assert isinstance(s.dataframes[i], pd.DataFrame)

    # Check that comments aren't included in df
    assert s.dataframes[0].shape == (1, 1)


def test_read_rln31():
    """
    Check that reading of RELION 3.1 style star files works properly
    """
    sf = StarParser(rln31_style)
    for idx, df in enumerate(sf.dataframes):
        assert isinstance(df, pd.DataFrame)
        if idx == 0:
            assert df.shape == (1, 7)
            pass
        else:
            assert df.shape == (2, 5)


def test_read_n_blocks():
    """
    Check that passing read_n_blocks allows reading of only a specified
    number of data blocks from a star file
    """
    # test 1 block
    sf = StarParser(postprocess, read_n_blocks=1)
    assert len(sf.dataframes) == 1

    # test 2 blocks
    sf = StarParser(postprocess, read_n_blocks=2)
    assert len(sf.dataframes) == 2


def test_single_line_middle_of_multiblock():
    sf = StarParser(single_line_middle_of_multiblock)
    assert len(sf.dataframes) == 2


def test_single_line_end_of_multiblock():
    sf = StarParser(single_line_end_of_multiblock)
    assert len(sf.dataframes) == 2
    assert sf.dataframes[-1].shape[0] == 1


def test_read_optimiser_2d():
    sf = StarParser(optimiser_2d)
    assert len(sf.dataframes) == 1
    assert sf.data.shape == (1, 84)


def test_read_optimiser_3d():
    sf = StarParser(optimiser_3d)
    assert len(sf.dataframes) == 1
    assert sf.data.shape == (1, 84)


def test_read_sampling_2d():
    sf = StarParser(sampling_2d)
    assert len(sf.dataframes) == 1
    assert sf.data.shape == (1, 12)


def test_read_sampling_3d():
    sf = StarParser(sampling_3d)
    assert len(sf.dataframes) == 2
    assert sf.dataframes['sampling_general'].shape == (1, 15)
    assert sf.dataframes['sampling_directions'].shape == (192, 2)
