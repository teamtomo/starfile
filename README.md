# starfile
[![License](https://img.shields.io/pypi/l/starfile.svg?color=green)](https://github.com/teamtomo/starfile/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/starfile.svg?color=green)](https://pypi.org/project/starfile)
[![Python Version](https://img.shields.io/pypi/pyversions/starfile.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/starfile/actions/workflows/ci.yml/badge.svg)](https://github.com/teamtomo/starfile/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/teamtomo/starfile/branch/main/graph/badge.svg)](https://codecov.io/gh/teamtomo/starfile)


*starfile* is a package for reading and writing
[STAR files](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval) in Python.

<p align="center" width="100%">
    <img width="70%" src="https://user-images.githubusercontent.com/7307488/204108873-c2175153-fb5b-4b22-892a-0a1274616057.png"> 
</p>

*starfile* can be used interactively to inspect/explore files or in 
scripts and larger software packages to provide basic STAR file I/O functions.
Data is exposed as simple python dictionaries or
[pandas dataframes](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe).

This package was designed principally for compatibility with files generated by
[RELION](https://www3.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page).

For more information on working with dataframes, please see the
[pandas docs](https://pandas.pydata.org/docs/user_guide/10min.html).

For *starfile* specific documentation, see [teamtomo.org/starfile](https://teamtomo.org/starfile)


---
# Quickstart
For the following file `particles.star` with a single data block

```txt
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

from src import starfile

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

Save the (modified) data to file

```python
starfile.write(df, 'modified_particles.star')
```

For more advanced usage please check out the examples.

---

# Installation

```shell
pip install starfile
```
