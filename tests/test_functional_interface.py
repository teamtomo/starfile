from pathlib import Path

import pandas as pd
import pytest
import starfile

from .constants import loop_simple, postprocess, test_df, test_data_directory


def test_read():
    df = starfile.read(loop_simple)
    assert isinstance(df, pd.DataFrame)


def test_read_always_dict():
    data = starfile.read(loop_simple, always_dict=True)
    assert isinstance(data, dict)


def test_read_multiblock():
    data = starfile.read(postprocess)
    assert isinstance(data, dict)
    assert len(data) == 3


def test_write():
    output_file = test_data_directory / 'test_write.star'
    starfile.write(test_df, output_file, overwrite=True)
    assert output_file.exists()


def test_write_fails_to_overwrite_without_flag():
    output_file = test_data_directory / 'test_overwrite_flag.star'
    starfile.write(test_df, output_file, overwrite=True)

    assert output_file.exists()
    with pytest.raises(FileExistsError):
        starfile.write(test_df, output_file, overwrite=False)
        starfile.new(test_df, output_file)


def test_write_overwrites_with_flag():
    output_file = test_data_directory / 'test_overwrite_flag.star'
    starfile.write(test_df, output_file, overwrite=True)

    assert output_file.exists()
    starfile.write(test_df, output_file, overwrite=True)


def test_write_with_float_format():
    output_file = test_data_directory / 'test_write_with_float_format.star'
    test_df['float_col'] = 1.23456789
    starfile.write(test_df, output_file, float_format='%.3f', overwrite=True)
    assert output_file.exists()


def test_read_non_existent_file():
    f = Path('non-existent-file.star')
    assert f.exists() is False

    with pytest.raises(FileNotFoundError):
        starfile.read(f)
