from os.path import join as join_path
from tempfile import TemporaryDirectory

import pandas as pd

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

def test_string_quoting(tmp_path):
    df = pd.DataFrame([["String with space", " ", '"Already quoted string"']], columns=["string_space", "just_space", "already_quoted"])

    filename = tmp_path / "test.star"
    StarWriter(df, filename, force_loop=True)
    s = StarParser(filename)
    print(s)
    assert False

def test_string_quoting_simple_datablock(tmp_path):
    df = pd.DataFrame([["String with space", " ", '"Already quoted string"']], columns=["string_space", "just_space", "already_quoted"])

    filename = tmp_path / "test.star"
    StarWriter(df, filename)
    s = StarParser(filename)
    print(s)
    assert False