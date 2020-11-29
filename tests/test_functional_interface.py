# from pathlib import Path
#
# import pandas as pd
# import pytest
# import starfile
#
# from .constants import loop_simple, test_df, test_data
#
#
# def test_read():
#     df = starfile.open(loop_simple)
#     assert isinstance(df, pd.DataFrame)
#
#
# def test_write():
#     output_file = test_data / 'test_write.star'
#     starfile.new(test_df, output_file)
#     assert output_file.exists()
#
#
# def test_write_with_kwargs():
#     output_file = test_data / 'test_write_kwargs.star'
#     starfile.new(test_df, output_file, float_format='%.5f')
#     assert output_file.exists()
#
#
# def test_read_non_existent_file():
#     f = Path('non-existent-file.star')
#     assert f.exists() is False
#
#     with pytest.raises(FileNotFoundError):
#         starfile.read(f)
