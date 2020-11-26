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
optimiser_2d = relion_tutorial / 'run_it025_optimiser_2D.star'
optimiser_3d = relion_tutorial / 'run_it025_optimiser_3D.star'
sampling_2d = relion_tutorial / 'run_it025_sampling_2D.star'
sampling_3d = relion_tutorial / 'run_it025_sampling_3D.star'

# Example DataFrame for testing
cars = {'Brand': ['Honda_Civic', 'Toyota_Corolla', 'Ford_Focus', 'Audi_A4'],
        'Price': [22000, 25000, 27000, 35000]
        }
test_df = pd.DataFrame.from_dict(cars)
