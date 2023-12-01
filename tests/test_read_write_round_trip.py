from .constants import two_single_line_loop_blocks, postprocess

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