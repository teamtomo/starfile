from unittest import TestCase
from pathlib import Path
from starfile.starfile import StarFile

import pandas as pd


class test_StarFile(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_simple = Path().joinpath('data', 'one_loop.star')
        self.postprocess = Path().joinpath('data', 'postprocess.star')

    def test_instantiation(self):
        s = StarFile(self.loop_simple)

    def test_read_loopheader(self):
        s = StarFile(self.loop_simple)
        header, data_block_start = s._read_loop_header(4)
        self.assertTrue('rlnCoordinateX' in header)
        self.assertTrue(len(header) == 12)

    def test_read_loop_block(self):
        s = StarFile(self.loop_simple)
        df = s._read_loop_block(4, s.n_lines)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape == (1365, 12))

    def test_find_data_block_starts(self):
        s = StarFile(self.postprocess)
        db_starts = s._find_data_block_starts()
        self.assertTrue(db_starts == [4, 14, 75])

    def test_n_data_blocks(self):
        s = StarFile(self.postprocess)
        n_data_blocks = s.n_data_blocks
        self.assertTrue(n_data_blocks == 3)

    def test_read_data_block_simple(self):
        s = StarFile(self.postprocess)
        df = s._read_data_block(4, 14)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape == (1, 6))

    def test_read_file_loop(self):
        s = StarFile(self.loop_simple)
        s._read_file()
        self.assertTrue(len(s.dataframes) == 1)
        self.assertIsInstance(s.dataframes[0], pd.DataFrame)
        self.assertTrue(s.dataframes[0].shape == (1365, 12))

    def test_read_file_multiblock(self):
        s = StarFile(self.postprocess)
        s._read_file()
        self.assertTrue(len(s.dataframes) == 3)
        self.assertTrue(all([isinstance(s.dataframes[i], pd.DataFrame) for i in range(3)]))
        self.assertTrue(s.dataframes[0].shape == (1, 6))
        self.assertTrue(s.dataframes[1].shape == (49, 7))
        self.assertTrie(s.dataframes[2].shape == (49, 3))


