from unittest import TestCase
from pathlib import Path

import pandas as pd

import starfile

class TestFunctions(TestCase):
    def test_read(self):
        df = starfile.read(Path('data', 'one_loop.star'))
        self.assertIsInstance(df, pd.DataFrame)

    def test_write(self):
        cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
                'Price': [22000, 25000, 27000, 35000]
                }

        test_df = pd.DataFrame(cars, columns=['Brand', 'Price'])
        starfile.write(test_df, Path('data', 'test_write.star'))