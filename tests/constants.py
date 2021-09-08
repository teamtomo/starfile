from pathlib import Path

import pandas as pd

# Directories for test data
test_data = Path() / 'data'
relion_tutorial = test_data / 'relion_tutorial'

# Test files
loop_simple = test_data / 'one_loop.star'
postprocess = test_data / 'postprocess.star'
pipeline = test_data / 'default_pipeline.star'
rln31_style = test_data / 'rln3.1_data_style.star'
single_line_end_of_multiblock = test_data / 'single_line_end_of_multiblock.star'
single_line_middle_of_multiblock = test_data / 'single_line_middle_of_multiblock.star'
optimiser_2d = relion_tutorial / 'run_it025_optimiser_2D.star'
optimiser_3d = relion_tutorial / 'run_it025_optimiser_3D.star'
sampling_2d = relion_tutorial / 'run_it025_sampling_2D.star'
sampling_3d = relion_tutorial / 'run_it025_sampling_3D.star'
non_existant_file = test_data / 'non_existant_file.star'
two_single_line_loop_blocks = test_data / 'two_single_line_loop_blocks.star'
two_basic_blocks = test_data / 'two_basic_blocks.star'

# Example DataFrame for testing
cars = {'Brand': ['Honda_Civic', 'Toyota_Corolla', 'Ford_Focus', 'Audi_A4'],
        'Price': [22000, 25000, 27000, 35000]
        }
test_df = pd.DataFrame.from_dict(cars)


# Attributes of certain files
loop_simple_columns = ['rlnCoordinateX', 'rlnCoordinateY', 'rlnCoordinateZ',
       'rlnMicrographName', 'rlnMagnification', 'rlnDetectorPixelSize',
       'rlnCtfMaxResolution', 'rlnImageName', 'rlnCtfImage', 'rlnAngleRot',
       'rlnAngleTilt', 'rlnAnglePsi']
