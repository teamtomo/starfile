from os.path import join as join_path
from tempfile import TemporaryDirectory
import math 

import pandas as pd
import pytest

from starfile.parser import StarParser
from starfile.writer import StarWriter

from .constants import loop_simple, postprocess, test_data_directory, test_df


def test_write_simple_block():
    s = StarParser(postprocess)
    output_file = test_data_directory / 'basic_block.star'
    StarWriter(s.data_blocks, output_file)
    assert output_file.exists()


def test_write_loop():
    s = StarParser(loop_simple)
    output_file = test_data_directory / 'loop_block.star'
    StarWriter(s.data_blocks, output_file)
    assert output_file.exists()


def test_write_multiblock():
    s = StarParser(postprocess)
    output_file = test_data_directory / 'multiblock.star'
    StarWriter(s.data_blocks, output_file)
    assert output_file.exists()


def test_from_single_dataframe():
    output_file = test_data_directory / 'from_df.star'

    StarWriter(test_df, output_file)
    assert output_file.exists()

    s = StarParser(output_file)


def test_create_from_dataframes():
    dfs = [test_df, test_df]

    output_file = test_data_directory / 'from_list.star'
    StarWriter(dfs, output_file)
    assert output_file.exists()

    s = StarParser(output_file)
    assert len(s.data_blocks) == 2


def test_can_write_non_zero_indexed_one_row_dataframe():
    # see PR #13 - https://github.com/alisterburt/starfile/pull/13
    df = pd.DataFrame([[1, 2, 3]], columns=["A", "B", "C"])
    df.index += 1

    with TemporaryDirectory() as directory:
        filename = join_path(directory, "test.star")
        StarWriter(df, filename)
        with open(filename) as output_file:
            output = output_file.read()

    expected = (
        "_A #1\n"
        "_B #2\n"
        "_C #3\n"
        "1\t2\t3"
    )
    assert (expected in output)


@pytest.mark.parametrize("quotechar", ["'",'"'])
def test_string_quoting_loop_datablock(tmp_path):
    df = pd.DataFrame([["nospace", "String with space", " ", ""]],
                       columns=["string_without_space", "string_space", "just_space", "empty_string"])

    filename = tmp_path / "test.star"
    StarWriter(df, filename)
    
    # Only 3 strings should be quoted
    with open(filename) as f:
        star_content = f.read()
        assert star_content.count('"') == 6

    s = StarParser(filename)
    assert df.loc[0, "string_space"] == s.data_blocks[""].loc[0, "string_space"]
    assert df.loc[0, "just_space"] == s.data_blocks[""].loc[0, "just_space"]
    assert math.isnan(s.data_blocks[""].loc[0, "empty_string"])


@pytest.mark.parametrize("quotechar", ["'",'"'])
def test_string_quoting_simple_datablock(quotechar, tmp_path):
    o = {
        "string_without_space": "nospace",
        "string_space": "String with space",
        "just_space": " ",
        "empty_string": ""
    }

    filename = tmp_path / "test.star"
    StarWriter(o, filename, quotechar=quotechar)
    # Only 3 strings should be quoted
    with open(filename) as f:
        star_content = f.read()
        assert star_content.count(quotechar) == 6

    s = StarParser(filename)
    assert o["string_space"] == s.data_blocks[""]["string_space"]

