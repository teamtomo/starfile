from unittest import TestCase
from pathlib import Path
from starfile.starfile import StarFile

import pandas as pd


class TestStarFile(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_simple = Path().joinpath('test', 'data', 'one_loop.star')
        self.postprocess = Path().joinpath('test', 'data', 'postprocess.star')
        self.pipeline = Path().joinpath('test', 'data', 'default_pipeline.star')
        self.optics_group_rln31 = Path().joinpath('test', 'data', 'optics_group_inter1965_simpler.star')
        self.mmcif = Path().joinpath('test', 'data', '3ja6.cif')
        self.multi_line_c_engine = Path().joinpath('test', 'data', 'multi_line_c_engine.star')
        self.single_line_c_engine = Path().joinpath('test', 'data', 'single_line_c_engine.star')
        self.single_line_python_engine = Path().joinpath('test', 'data', 'single_line_python_engine.star')
        cars = {'Brand': ['Honda_Civic', 'Toyota_Corolla', 'Ford_Focus', 'Audi_A4'],
                'Price': [22000, 25000, 27000, 35000]
                }

        self.test_df = pd.DataFrame(cars, columns=['Brand', 'Price'])


    def test_instantiation(self):
        s = StarFile(self.loop_simple)

    def test_read_loopheader(self):
        s = StarFile(self.loop_simple)
        self.assertTrue('rlnCoordinateX' in s.data.columns)
        self.assertTrue(len(s.data.columns) == 12)

    def test_read_loop_block(self):
        s = StarFile(self.loop_simple)
        self.assertIsInstance(s.data, pd.DataFrame)
        self.assertTrue(s.data.shape == (1365, 12))

    def test_read_data_block_simple(self):
        s = StarFile(self.postprocess)
        s.line_number = 4
        s._read_data_block()
        self.assertIsInstance(s.dataframes[-1], pd.DataFrame)
        self.assertTrue(s.dataframes[-1].shape == (1, 6))

    def test_read_file_loop(self):
        s = StarFile(self.loop_simple)
        self.assertIsInstance(s.data, pd.DataFrame)
        self.assertTrue(s.data.shape == (1365, 12))

    def test_read_file_multiblock(self):
        s = StarFile(self.postprocess)
        self.assertTrue(len(s.dataframes) == 3)
        self.assertTrue(all([isinstance(s.dataframes[i], pd.DataFrame) for i in range(3)]))
        self.assertTrue(s.dataframes[0].shape == (1, 6))
        self.assertTrue(s.dataframes[1].shape == (49, 7))
        self.assertTrue(s.dataframes[2].shape == (49, 3))

    def test_write_excel(self):
        s = StarFile(self.postprocess)
        s.to_excel(Path('test', 'data', 'star2excel.xlsx'))


    def test_write_simple_block(self):
        s = StarFile(self.postprocess)
        s.dataframes = s.dataframes[0]
        s.write_star_file(Path('test', 'data', 'basic_block.star'))

    def test_write_loop(self):
        s = StarFile(self.loop_simple)
        s.write_star_file(Path('test', 'data', 'loop_block.star'))

    def test_write_multiblock(self):
        s = StarFile(self.postprocess)
        self.assertTrue(s.dataframes[0].name == 'general')
        s.write_star_file(Path('test', 'data', 'multiblock.star'))

    def test_create_from_dataframe(self):
        s = StarFile(data=self.test_df)
        self.assertIsInstance(s.data, pd.DataFrame)

    def test_create_from_dataframes(self):
        df = [self.test_df, self.test_df]
        s = StarFile(data=df)
        self.assertTrue(len(s.dataframes) == 2)
        self.assertIsInstance(s.dataframes[0], pd.DataFrame)

    def test_read_pipeline(self):
        s = StarFile(self.pipeline)
        self.assertIsInstance(s.dataframes, list)
        for i in range(5):
            self.assertIsInstance(s.dataframes[i], pd.DataFrame)

        # Check that comments are handled properly for blocks now and aren't included in df
        self.assertTrue(s.dataframes[0].shape == (1, 1))


    def test_read_optics_group_inter1965(self):
        sf = StarFile(self.optics_group_rln31)
        for idx, df in enumerate(sf.dataframes):
            self.assertIsInstance(df, pd.DataFrame)
            if idx == 0:
                self.assertTrue(df.shape == (1, 7))
                pass
            else:
                self.assertTrue(df.shape == (2, 5))

    def test_multi_line_c_engine(self):
        sf = StarFile(self.multi_line_c_engine)
        for df in sf.dataframes:
            self.assertTrue(df.shape == (2, 5))

    def test_single_line_c_engine(self):
        sf = StarFile(self.single_line_c_engine)
        df_last = sf.dataframes[-1]
        self.assertTrue(df_last.shape == (1, 5))

    def test_single_line_python_engine(self):
        sf = StarFile(self.single_line_python_engine)
        df_first = sf.dataframes[0]
        self.assertTrue(df_first.shape == (1, 5))

