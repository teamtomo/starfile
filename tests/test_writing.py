from os.path import join as join_path
from tempfile import TemporaryDirectory

import pandas as pd

from starfile.parser import StarParser
from starfile.writer import StarWriter

from .constants import loop_simple, postprocess, pipeline, rln31_style, optimiser_2d, optimiser_3d, sampling_2d, \
    sampling_3d, test_data_directory, test_df


def test_write_simple_block():
    s = StarParser(postprocess)
    output_file = test_data_directory / 'basic_block.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_write_loop():
    s = StarParser(loop_simple)
    output_file = test_data_directory / 'loop_block.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_write_multiblock():
    s = StarParser(postprocess)
    output_file = test_data_directory / 'multiblock.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_from_single_dataframe():
    output_file = test_data_directory / 'from_df.star'

    StarWriter(test_df, output_file, overwrite=True)
    assert output_file.exists()

    s = StarParser(output_file)


def test_create_from_dataframes():
    dfs = [test_df, test_df]

    output_file = test_data_directory / 'from_list.star'
    StarWriter(dfs, output_file, overwrite=True)
    assert output_file.exists()

    s = StarParser(output_file)
    assert len(s.dataframes) == 2

def test_can_write_non_zero_indexed_one_row_dataframe():
    # see PR #13 - https://github.com/alisterburt/starfile/pull/13
    df = pd.DataFrame([[1,2,3]], columns=["A", "B", "C"])
    df.index += 1

    with TemporaryDirectory() as directory:
        filename = join_path(directory, "test.star")
        StarWriter(df, filename)
        with open(filename) as output_file:
            output = output_file.read()

    expected = (
        "_A\t\t\t1\n"
        "_B\t\t\t2\n"
        "_C\t\t\t3\n"
    )
    assert (expected in output)
