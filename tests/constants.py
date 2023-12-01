from pathlib import Path

import pandas as pd

# Directories for test data
test_data_directory = Path(__file__).parent / 'data'
relion_tutorial = test_data_directory / 'relion_tutorial'

# Test files
loop_simple = test_data_directory / 'one_loop.star'
postprocess = test_data_directory / 'postprocess.star'
pipeline = test_data_directory / 'default_pipeline.star'
rln31_style = test_data_directory / 'rln3.1_data_style.star'
single_line_end_of_multiblock = test_data_directory / 'single_line_end_of_multiblock.star'
single_line_middle_of_multiblock = test_data_directory / 'single_line_middle_of_multiblock.star'
optimiser_2d = relion_tutorial / 'run_it025_optimiser_2D.star'
optimiser_3d = relion_tutorial / 'run_it025_optimiser_3D.star'
sampling_2d = relion_tutorial / 'run_it025_sampling_2D.star'
sampling_3d = relion_tutorial / 'run_it025_sampling_3D.star'
non_existant_file = test_data_directory / 'non_existant_file.star'
two_single_line_loop_blocks = test_data_directory / 'two_single_line_loop_blocks.star'
two_basic_blocks = test_data_directory / 'two_basic_blocks.star'
empty_loop = test_data_directory / 'empty_loop.star'
basic_single_quote = test_data_directory / 'basic_single_quote.star'
basic_double_quote = test_data_directory / 'basic_double_quote.star'
loop_single_quote = test_data_directory / 'loop_single_quote.star'
loop_double_quote = test_data_directory / 'loop_double_quote.star'

# Example DataFrame for testing
cars = {'Brand': ['Honda_Civic', 'Toyota_Corolla', 'Ford_Focus', 'Audi_A4'],
        'Price': [22000, 25000, 27000, 35000]
        }
test_df = pd.DataFrame.from_dict(cars)
