from pathlib import Path
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
    two_single_line_loop_blocks,
    two_basic_blocks,
    empty_loop,
    basic_single_quote,
    basic_double_quote,
    loop_single_quote,
    loop_double_quote,
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
    parser = StarParser(loop_simple)

    # Check that only one object is present
    assert len(parser.data_blocks) == 1

    # get dataframe
    df = list(parser.data_blocks.values())[0]
    assert isinstance(df, pd.DataFrame)

    # Check shape of dataframe
    assert df.shape == (16, 12)

    # check columns
    expected_columns = [
        'rlnCoordinateX',
        'rlnCoordinateY',
        'rlnCoordinateZ',
        'rlnMicrographName',
        'rlnMagnification',
        'rlnDetectorPixelSize',
        'rlnCtfMaxResolution',
        'rlnImageName',
        'rlnCtfImage',
        'rlnAngleRot',
        'rlnAngleTilt',
        'rlnAnglePsi',
    ]
    assert all(df.columns == expected_columns)


def test_read_multiblock_file():
    """
    Check that multiblock STAR files such as postprocess RELION files
    parse properly
    """
    parser = StarParser(postprocess)
    assert len(parser.data_blocks) == 3

    assert 'general' in parser.data_blocks
    assert isinstance(parser.data_blocks['general'], dict)
    assert len(parser.data_blocks['general']) == 6
    columns = list(parser.data_blocks['general'].keys())
    expected_columns = [
        'rlnFinalResolution',
        'rlnBfactorUsedForSharpening',
        'rlnUnfilteredMapHalf1',
        'rlnUnfilteredMapHalf2',
        'rlnMaskName',
        'rlnRandomiseFrom',
    ]
    assert columns == expected_columns

    assert 'fsc' in parser.data_blocks
    assert isinstance(parser.data_blocks['fsc'], pd.DataFrame)
    assert parser.data_blocks['fsc'].shape == (49, 7)

    assert 'guinier' in parser.data_blocks
    assert isinstance(parser.data_blocks['guinier'], pd.DataFrame)
    assert parser.data_blocks['guinier'].shape == (49, 3)


def test_read_pipeline():
    """
    Check that a pipeline.star file is parsed correctly
    """
    parser = StarParser(pipeline)

    # Check that data match file contents
    assert isinstance(parser.data_blocks['pipeline_general'], dict)
    assert parser.data_blocks['pipeline_processes'].shape == (31, 4)
    assert parser.data_blocks['pipeline_nodes'].shape == (74, 2)
    assert parser.data_blocks['pipeline_input_edges'].shape == (48, 2)
    assert parser.data_blocks['pipeline_output_edges'].shape == (72, 2)


def test_read_rln31():
    """
    Check that reading of RELION 3.1 style star files works properly
    """
    s = StarParser(rln31_style)

    for key, df in s.data_blocks.items():
        assert isinstance(df, pd.DataFrame)

    assert isinstance(s.data_blocks['block_1'], pd.DataFrame)
    assert isinstance(s.data_blocks['block_2'], pd.DataFrame)
    assert isinstance(s.data_blocks['block_3'], pd.DataFrame)


def test_read_n_blocks():
    """
    Check that passing read_n_blocks allows reading of only a specified
    number of data blocks from a star file
    """
    # test 1 block
    s = StarParser(postprocess, n_blocks_to_read=1)
    assert len(s.data_blocks) == 1

    # test 2 blocks
    s = StarParser(postprocess, n_blocks_to_read=2)
    assert len(s.data_blocks) == 2


def test_single_line_middle_of_multiblock():
    s = StarParser(single_line_middle_of_multiblock)
    assert len(s.data_blocks) == 2


def test_single_line_end_of_multiblock():
    s = StarParser(single_line_end_of_multiblock)
    assert len(s.data_blocks) == 2

    # iterate over dataframes, checking keys, names and shapes
    for idx, (key, df) in enumerate(s.data_blocks.items()):
        if idx == 0:
            assert key == 'block_1'
            assert df.shape == (2, 5)
        if idx == 1:
            assert key == 'block_2'
            assert df.shape == (1, 5)


def test_read_optimiser_2d():
    parser = StarParser(optimiser_2d)
    assert len(parser.data_blocks) == 1
    assert len(parser.data_blocks['optimiser_general']) == 84


def test_read_optimiser_3d():
    parser = StarParser(optimiser_3d)
    assert len(parser.data_blocks) == 1
    assert len(parser.data_blocks['optimiser_general']) == 84


def test_read_sampling_2d():
    parser = StarParser(sampling_2d)
    assert len(parser.data_blocks) == 1
    assert len(parser.data_blocks['sampling_general']) == 12


def test_read_sampling_3d():
    parser = StarParser(sampling_3d)
    assert len(parser.data_blocks) == 2
    assert len(parser.data_blocks['sampling_general']) == 15
    assert parser.data_blocks['sampling_directions'].shape == (192, 2)


def test_parsing_speed():
    generate_large_star_file()
    start = time.time()
    s = StarParser(million_row_file)
    end = time.time()
    remove_large_star_file()

    # Check that execution takes less than a second
    assert end - start < 1.0


def test_two_single_line_loop_blocks():
    parser = StarParser(two_single_line_loop_blocks)
    assert len(parser.data_blocks) == 2

    np.testing.assert_array_equal(
        parser.data_blocks['block_0'].columns, [f'val{i}' for i in (1, 2, 3)]
    )
    assert parser.data_blocks['block_0'].shape == (1, 3)

    np.testing.assert_array_equal(
        parser.data_blocks['block_1'].columns, [f'col{i}' for i in (1, 2, 3)]
    )
    assert parser.data_blocks['block_1'].shape == (1, 3)


def test_two_basic_blocks():
    parser = StarParser(two_basic_blocks)
    assert len(parser.data_blocks) == 2
    assert 'block_0' in parser.data_blocks
    b0 = parser.data_blocks['block_0']
    assert b0 == {
        'val1': 1.0,
        'val2': 2.0,
        'val3': 3.0,
    }
    assert 'block_1' in parser.data_blocks
    b1 = parser.data_blocks['block_1']
    assert b1 == {
        'col1': 'A',
        'col2': 'B',
        'col3': 'C',
    }


def test_empty_loop_block():
    """Parsing an empty loop block should return an empty dataframe."""
    parser = StarParser(empty_loop)
    assert len(parser.data_blocks) == 1


@pytest.mark.parametrize("quote_character, filename", [("'", basic_single_quote),
                                                       ('"', basic_double_quote),
                                                       ])
def test_quote_basic(quote_character, filename):
    parser = StarParser(filename)
    assert len(parser.data_blocks) == 1
    assert parser.data_blocks['']['no_quote_string'] == "noquote"
    assert parser.data_blocks['']['quote_string'] == "quote string"
    assert parser.data_blocks['']['whitespace_string'] == " "
    assert parser.data_blocks['']['empty_string'] == ""


@pytest.mark.parametrize("quote_character, filename", [("'", loop_single_quote),
                                                       ('"', loop_double_quote),
                                                       ])
def test_quote_loop(quote_character, filename):
    import math
    parser = StarParser(filename)
    assert len(parser.data_blocks) == 1
    assert parser.data_blocks[''].loc[0, 'no_quote_string'] == "noquote"
    assert parser.data_blocks[''].loc[0, 'quote_string'] == "quote string"
    assert parser.data_blocks[''].loc[0, 'whitespace_string'] == " "
    assert parser.data_blocks[''].loc[0, 'empty_string'] == ""

    assert parser.data_blocks[''].dtypes['number_and_string'] == object
    assert parser.data_blocks[''].dtypes['number_and_empty'] == 'float64'
    assert parser.data_blocks[''].dtypes['number'] == 'float64'
    assert parser.data_blocks[''].dtypes['empty_string_and_normal_string'] == object

    assert math.isnan(parser.data_blocks[''].loc[1, 'number_and_empty'])
    assert parser.data_blocks[''].loc[0, 'empty_string_and_normal_string'] == ''


def test_parse_as_string():
    parser = StarParser(postprocess, parse_as_string=['rlnFinalResolution', 'rlnResolution'])

    # check 'rlnFinalResolution' is parsed as string in general (basic) block
    block = parser.data_blocks['general']
    assert type(block['rlnFinalResolution']) == str

    # check 'rlnResolution' is parsed as string in fsc (loop) block
    df = parser.data_blocks['fsc']
    assert df['rlnResolution'].dtype == 'object'


def test_parse_na(tmpdir):
    import starfile

    parts = pd.DataFrame({"property1": np.arange(10), "property2": np.random.rand(10)})
    parts["property2"].values[-1] *= np.nan
    data = {
        "particles": parts
    }
    tmpfile = Path(tmpdir) / "temp.star"
    starfile.write(data, tmpfile) 
    data = starfile.read(tmpfile)
    assert data["property2"].dtype == "float64"
