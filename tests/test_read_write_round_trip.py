import time

import pandas.testing

from .constants import two_single_line_loop_blocks, postprocess, loop_simple

import starfile
import pandas as pd


def test_round_trip_two_single_line_loop_blocks(tmp_path):
    # read
    expected = starfile.read(two_single_line_loop_blocks)

    # write
    output_file = tmp_path / 'two_single_line_loop_blocks.star'
    starfile.write(expected, output_file)

    # read
    star_after_round_trip = starfile.read(output_file)

    # assert
    for expected_df, actual_df in zip(expected.values(), star_after_round_trip.values()):
        pd.testing.assert_frame_equal(expected_df, actual_df)


def test_round_trip_postprocess(tmp_path):
    expected = starfile.read(postprocess)

    # write
    output_file = tmp_path / 'two_single_line_loop_blocks.star'
    starfile.write(expected, output_file)

    # read
    star_after_round_trip = starfile.read(output_file)

    # assert
    for _expected, _actual in zip(expected.values(), star_after_round_trip.values()):
        if isinstance(_actual, pd.DataFrame):
            pd.testing.assert_frame_equal(_actual, _expected, atol=1e-6)
        else:
            assert _actual == _expected


def test_write_read_write_read(tmp_path):
    filename = tmp_path / 'tmp.star'
    df_a = pd.DataFrame({'a': [0, 1], 'b': [2, 3]})
    starfile.write(df_a, filename)

    df_b = pd.DataFrame({'c': [0, 1], 'd': [2, 3]})
    starfile.write(df_b, filename)

    df_b_read = starfile.read(filename)
    pandas.testing.assert_frame_equal(df_b, df_b_read)


def test_dataframe_name_magic(tmp_path):
    function_read = starfile.read(loop_simple)
    assert function_read.name == 'particles', "Expected the name of the DataFrame to be 'particles'."

    starfile.write(function_read, tmp_path / 'tmp.star')

    # Make sure tmp.star contains data_particles
    with open(tmp_path / 'tmp.star') as f:
        content = f.read()
        assert 'data_particles' in content, "Expected 'data_particles' in the STAR file content."
