from unittest import TestCase
from pathlib import Path

import pandas as pd

import starfile

class TestFunctions(TestCase):
    def test_read(self):
        df = starfile.open(Path('test', 'data', 'one_loop.star'))
        self.assertIsInstance(df, pd.DataFrame)

    def test_write(self):
        cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
                'Price': [22000, 25000, 27000, 35000]
                }

        test_df = pd.DataFrame(cars, columns=['Brand', 'Price'])
        starfile.new(test_df, Path('test', 'data', 'test_write.star'))
        self.assertTrue(Path('test','data','test_write.star').exists())

    def test_write_with_kwargs(self):
        cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
                'Price': [22000.12345668, 25.525534, 27.99999999999999, 35.830392383379393939393837474]
                }

        test_df = pd.DataFrame(cars, columns=['Brand', 'Price'])
        starfile.new(test_df, Path('test', 'data', 'test_write_kwargs.star'), float_format='%.5f')
        self.assertTrue(Path('test','data','test_write_kwargs.star').exists())