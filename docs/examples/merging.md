# merging data across tables

In this example, we will use pandas to merge data from two blocks in a 
RELION particle STAR file `particles.star`.

In RELION (`>=3.1`) particle STAR files contain an `optics` table and a `particles` table.
Data about `optics` common to many `particles` is stored in the `optics` table.


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

The column `rlnOpticsGroup` is present in both tables.

Merging data from multiple dataframes is an example of a **join** in 
[relational algebra](https://en.wikipedia.org/wiki/Relational_algebra#Joins_and_join-like_operators).
In pandas, this is implemented as 
[`DataFrame.merge()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).

```python

import starfile

star = starfile.read('particles.star')
df = star['particles'].merge(star['optics'], on='rlnOpticsGroup')
```

The resulting dataframe contains columns with data from both the `particles` and `optics` dataframes.

```python
df.head()
```
```txt
   rlnCoordinateX  rlnCoordinateY  rlnCoordinateZ  rlnAngleRot  rlnAngleTilt  ...  rlnSphericalAberration rlnVoltage rlnImagePixelSize  rlnImageSize  rlnImageDimensionality
0        880.2740        895.0579       1107.2450    131.24600     106.82080  ...                     2.7      300.0               3.3           160                       3
1        973.1655        958.6418       1115.1010     87.24711     109.23650  ...                     2.7      300.0               3.3           160                       3
2        955.9494        960.4651        629.4591      9.33137      99.30998  ...                     2.7      300.0               3.3           160                       3
3       1175.1770       1135.7310        882.6052   -147.26120      81.60538  ...                     2.7      300.0               3.3           160                       3
4       1190.6580       1122.1020       1073.6420     40.40459      98.06177  ...                     2.7      300.0               3.3           160                       3

[5 rows x 27 columns]

```

This table has the following properties
- every column is a variable 
- every row is an observation
- every cell contains a single value

Data in this form is sometimes referred to as 
[tidy data](https://vita.had.co.nz/papers/tidy-data.html). 
Tidy data is easier to manipulate.
