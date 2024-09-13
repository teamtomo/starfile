# multiple data block example

In this example, we will use *starfile* to read and write files containing multiple data blocks.

```txt title="particles.star"
data_optics

loop_
_rlnOpticsGroup #1
_rlnOpticsGroupName #2
_rlnSphericalAberration #3
_rlnVoltage #4
_rlnImagePixelSize #5
_rlnImageSize #6
_rlnImageDimensionality #7
1	opticsGroup1	2.700000	300.000000	3.300000	160	3

data_particles

loop_
_rlnCoordinateX #1
_rlnCoordinateY #2
_rlnCoordinateZ #3
_rlnAngleRot #4
_rlnAngleTilt #5
_rlnAnglePsi #6
_rlnImageName #7
_rlnCtfImage #8
_rlnRandomSubset #9
_rlnPixelSize #10
_rlnMicrographName #11
_rlnOpticsGroup #12
_rlnGroupNumber #13
_rlnOriginXAngst #14
_rlnOriginYAngst #15
_rlnOriginZAngst #16
_rlnClassNumber #17
_rlnNormCorrection #18
_rlnLogLikeliContribution #19
_rlnMaxValueProbDistribution #20
_rlnNrOfSignificantSamples #21
880.274000	895.057900	1107.245000	131.246000	106.820800	45.228430	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000000_3.30A.mrc	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000000_ctf_3.30A.mrc	2	3.300000	TS.mrc.tomostar	1	1	0.000000	0.000000	0.000000	6	1.000000	4150981.000000	1.000000	1
973.165500	958.641800	1115.101000	87.247110	109.236500	45.323810	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000001_3.30A.mrc	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000001_ctf_3.30A.mrc	1	3.300000	TS.mrc.tomostar	1	1	0.000000	0.000000	0.000000	4	1.000000	4150837.000000	1.000000	1
955.949400	960.465100	629.459100	9.331370	99.309980	11.024810	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000002_3.30A.mrc	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000002_ctf_3.30A.mrc	1	3.300000	TS.mrc.tomostar	1	1	0.000000	0.000000	0.000000	3	1.000000	4150650.000000	1.000000	1
1175.177000	1135.731000	882.605200	-147.261200	81.605380	77.325710	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000003_3.30A.mrc	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000003_ctf_3.30A.mrc	2	3.300000	TS.mrc.tomostar	1	1	0.000000	0.000000	0.000000	1	1.000000	4151420.000000	1.000000	1
1190.658000	1122.102000	1073.642000	40.404590	98.061770	42.563060	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000004_3.30A.mrc	subtomo_05Feb21/TS.mrc/TS.mrc_22redo_combined_0000004_ctf_3.30A.mrc	1	3.300000	TS.mrc.tomostar	1	1	0.000000	0.000000	0.000000	6	1.000000	4150168.000000	1.000000	1
```

## Reading
Reading a file with multiple data blocks is similar to reading a file with a single data block.
In this case, a dictionary of dataframes or dictionaries is returned. The keys of this dictionary are the names
of data blocks.

```python

import starfile

star = starfile.read('particles.star')
optics_df = star['optics']
particle_df = star['particles']
```

!!! tip
    
    `starfile.read` can be forced to always return a dictionary of entries.

    ```python
    starfile.read('particles.star', always_dict=True)
    ```

## Writing
Writing a file containing multiple data blocks is similar, simply pass a dictionary of entries.

```python

import starfile

starfile.write(
    {'optics': optics_df, 'particles': particle_df}, 'new_file.star'
)
```

