import pandas as pd

from starfile.parser import StarParser
from starfile.writer import StarWriter

from .constants import loop_simple, postprocess, pipeline, rln31_style, optimiser_2d, optimiser_3d, sampling_2d, \
    sampling_3d, test_data, test_df


def test_write_simple_block():
    s = StarParser(postprocess)
    output_file = test_data / 'basic_block.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_write_loop():
    s = StarParser(loop_simple)
    output_file = test_data / 'loop_block.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_write_multiblock():
    s = StarParser(postprocess)
    output_file = test_data / 'multiblock.star'
    StarWriter(s.dataframes, output_file, overwrite=True)
    assert output_file.exists()


def test_from_single_dataframe():
    output_file = test_data / 'from_df.star'

    StarWriter(test_df, output_file, overwrite=True)
    assert output_file.exists()

    s = StarParser(output_file)


def test_create_from_dataframes():
    dfs = [test_df, test_df]

    output_file = test_data / 'from_list.star'
    StarWriter(dfs, output_file, overwrite=True)
    assert output_file.exists()

    s = StarParser(output_file)
    assert len(s.dataframes) == 2
