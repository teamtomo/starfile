import pandas as pd

from starfile.parser import StarParser

from .constants import loop_simple, postprocess, pipeline, rln31_style, optimiser_2d, optimiser_3d, sampling_2d, \
    sampling_3d, test_data, test_df


def test_write_simple_block():
    s = StarParser(postprocess)
    output_file = test_data / 'basic_block.star'
    s.write_star_file(output_file)
    assert output_file.exists()


def test_write_loop():
    s = StarParser(loop_simple)
    output_file = test_data / 'loop_block.star'
    s.write_star_file(output_file)
    assert output_file.exists()


def test_write_multiblock():
    s = StarParser(postprocess)
    output_file = test_data / 'multiblock.star'
    s.write_star_file(output_file)
    assert output_file.exists()


def test_create_from_dataframe():
    s = StarParser(data=test_df)
    assert isinstance(s.data, pd.DataFrame)


def test_create_from_dataframes():
    df = [test_df, test_df]
    s = StarParser(data=df)
    assert len(s.dataframes) == 2
    assert isinstance(s.dataframes[0], pd.DataFrame)
