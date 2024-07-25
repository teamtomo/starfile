# single data block example

In this example, we will use *starfile* to read and write a STAR file with a single data block.

```txt title="particles.star"
data_particles

loop_
_rlnCoordinateX #1
_rlnCoordinateY #2
_rlnCoordinateZ #3
_rlnAngleRot #4
_rlnAngleTilt #5
_rlnAnglePsi #6
_rlnMicrographName #7
91.798700	83.622600	203.341030	-51.740000	173.930000	32.971000	01_10.00Apx.mrc
97.635800	80.437000	203.136160	141.500000	171.760000	-134.680000	01_10.00Apx.mrc
92.415200	88.842700	210.663900	-78.750000	173.930000	87.263200	01_10.00Apx.mrc
94.607830	93.135410	205.425960	-85.215000	167.170000	85.632200	01_10.00Apx.mrc
86.187800	80.125400	204.558750	14.910000	163.260000	-16.030000	01_10.00Apx.mrc
91.824240	76.738300	203.794280	39.740000	168.410000	-57.250000	01_10.00Apx.mrc
98.253300	73.530100	203.856030	73.950000	166.380000	-84.640000	01_10.00Apx.mrc
101.303500	80.290800	194.790400	-178.878000	166.090000	73.181000	01_10.00Apx.mrc
```

Read the file

```python

import starfile

df = starfile.read('particles.star')
```

Interact with the data

```python
df['rlnCoordinateX'] += 10
df.head()
```
```txt
   rlnCoordinateX  rlnCoordinateY  rlnCoordinateZ  rlnAngleRot  rlnAngleTilt  rlnAnglePsi rlnMicrographName
0       101.79870        83.62260       203.34103      -51.740        173.93      32.9710   01_10.00Apx.mrc
1       107.63580        80.43700       203.13616      141.500        171.76    -134.6800   01_10.00Apx.mrc
2       102.41520        88.84270       210.66390      -78.750        173.93      87.2632   01_10.00Apx.mrc
3       104.60783        93.13541       205.42596      -85.215        167.17      85.6322   01_10.00Apx.mrc
4        96.18780        80.12540       204.55875       14.910        163.26     -16.0300   01_10.00Apx.mrc
```


!!! note

    Simple data blocks (unlike those using the `loop_` notation) will return a python dictionary instead of a dataframe:


Save the (modified) data to file

```python
starfile.write(df, 'modified_particles.star')
```

For files containing multiple data blocks, please see the
[multiple data block](./multi_block.md) example.
