from pathlib import Path

import pandas as pd

from starfile.starfile import StarFile
from .constants import loop_simple, postprocess, pipeline, rln31_style, optimiser_2d, optimiser_3d, sampling_2d, \
    sampling_3d, single_line_middle_of_multiblock, single_line_end_of_multiblock


def test_instantiation():
    """
    Tests instantiation of the StarFile class
    """
    s = StarFile()


def test_read_loopheader():
    """
    Check that a simple loop block header is parsed correctly by the
    read_loopheader method by checking the dataframe columns
    """
    s = StarFile(loop_simple)
    assert 'rlnCoordinateX' in s.data.columns
    assert len(s.data.columns) == 12


def test_read_loop_block():
    """
    Check that loop block is parsed correctly, data has the correct shape
    """
    s = StarFile(loop_simple)
    assert isinstance(s.data, pd.DataFrame)
    assert s.data.shape == (16, 12)


def test_read_data_block_simple():
    """
    Check that simple data blocks (no loops) are read correctly
    """
    s = StarFile(postprocess)
    s.line_number = 4
    s._read_data_block()
    assert isinstance(s.dataframes[-1], pd.DataFrame)
    assert s.dataframes[-1].shape == (1, 6)


def test_read_file_multiblock():
    """
    Check that multiblock STAR files such as postprocess RELION files
    parse properly
    """
    s = StarFile(postprocess)
    assert len(s.dataframes) == 3
    assert all([isinstance(s.dataframes[i], pd.DataFrame) for i in range(3)])
    assert s.dataframes[0].shape == (1, 6)
    assert s.dataframes[1].shape == (49, 7)
    assert s.dataframes[2].shape == (49, 3)


def test_read_pipeline():
    """
    Check that a pipeline.star file is parsed correctly
    """
    s = StarFile(pipeline)
    assert isinstance(s.dataframes, list)
    for i in range(5):
        assert isinstance(s.dataframes[i], pd.DataFrame)

    # Check that comments aren't included in df
    assert s.dataframes[0].shape == (1, 1)

def test_read_rln31():
    """
    Check that reading of RELION 3.1 style star files works properly
    """
    sf = StarFile(rln31_style)
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
    sf = StarFile(postprocess, read_n_blocks=1)
    assert len(sf.dataframes) == 1


def test_single_line_middle_of_multiblock():
    sf = StarFile(single_line_middle_of_multiblock)
    assert len(sf.dataframes) == 2


def test_single_line_end_of_multiblock():
    sf = StarFile(single_line_end_of_multiblock)
    assert len(sf.dataframes) == 2

def test_read_optimiser_2d():
    sf = StarFile(optimiser_2d)
    assert len(sf.dataframes) == 1


def test_read_optimiser_3d():
    sf = StarFile(optimiser_3d)
    assert len(sf.dataframes) == 1


def test_read_sampling_2d():
    sf = StarFile(sampling_2d)
    assert len(sf.dataframes) == 1


def test_read_sampling_3d():
    sf = StarFile(sampling_3d)
    assert len(sf.dataframes) == 2
