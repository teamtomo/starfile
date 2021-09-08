# starfile
[![Build Status](https://travis-ci.com/alisterburt/starfile.svg?branch=master)](https://travis-ci.com/alisterburt/starfile)
[![PyPI version](https://badge.fury.io/py/starfile.svg)](https://pypi.python.org/pypi/starfile/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/starfile.svg)](https://pypi.python.org/pypi/starfile/)
[![DOI](https://zenodo.org/badge/273026988.svg)](https://zenodo.org/badge/latestdoi/273026988)


`starfile` is a Python implementation of the [STAR](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval) 
file format designed principally for compatibility with [RELION](https://github.com/3dem/relion)
 format STAR files.

It allows STAR files to be created and opened easily using a very simple API, exposing data blocks as [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html) `DataFrame` objects.

This library aims to allow users and developers to read and write STAR files in Python as easily as possible as well as to encourage further analysis of data within the scientific Python ([SciPy](https://www.scipy.org/)) ecosystem.

You can use it interactively to inspect/explore files or in scripts and larger software packages to provide basic STAR file I/O functions.

```
The STAR file: a new format for electronic dataframes transfer and archiving
J. Chem. Inf. Comput. Sci. 1991, 31, 2, 326–333
Publication Date: May 1, 1991
https://doi.org/10.1021/ci00002a020
```
## Features
- Easy to install and use
- Simple API for reading of STAR files as pandas `DataFrame` objects
- Simple API for writing of STAR files from pandas `DataFrame` objects


## Installation
Installation is available directly from the [Python package index](https://pypi.org/project/starfile/)
```bash
pip install starfile
```


## Usage

### Reading STAR files
To open a STAR file
```python
>>> import starfile
>>> df = starfile.open('tests/dataframes/one_loop.star')
>>> df
      rlnCoordinateX  rlnCoordinateY  ...  rlnAngleTilt rlnAnglePsi
0           1572.444        1084.500  ...             0           0
1           1507.500        1104.357  ...             0           0
2           1512.432         973.500  ...             0           0
3           1560.385        1063.500  ...             0           0
4           1537.500        1060.500  ...             0           0
              ...             ...  ...           ...         ...
1360        1078.500         796.500  ...             0           0
1361        1075.500         784.500  ...             0           0
1362        1080.531         796.500  ...             0           0
1363        1045.992         737.411  ...             0           0
1364        1053.530         745.500  ...             0           0

[1365 rows x 12 columns]
```

- Opening STAR files containing multiple dataframes blocks will return a `dict` of DataFrame objects.
- If you would like to always return a `dict`, you can use the `always_dict=True` keyword argument

This functionality is also exposed by `starfile.read` for convenience.

### Writing STAR files
DataFrame objects (or dicts or lists of dataframes) can be written to STAR files using `starfile.write`

```python
>>> starfile.write(df, 'tests/dataframes/cars.star')
```

Produces a STAR file which looks like
```bash
# Created by the starfile python package (version 0.1) on 18/06/2020 13:26:32

data_cars

loop_
_Brand #1
_Price #2
Honda_Civic	22000
Toyota_Corolla	25000
Ford_Focus	27000
Audi_A4	        35000
```


- floating point format can be specified by the `float_format` keyword argument (default `%.6f`)
- data block headers are of format `data_<key>` where key is the dictionary key if a `dict` is passed, `df.name` if a 
`DataFrame` or list of `DataFrame`s is passed

This functionality is also exposed by `starfile.write` for convenience.

## License
The project is released under the BSD 3-Clause License

## Testing
The project is tested using [pytest](https://docs.pytest.org/en/stable/). 
To run tests, simply run `pytest` in the `tests` directory

## Known Issues
- Cannot handle more than one loop in a data block as found in mmCIF files, please use 
[GEMMI](https://github.com/project-gemmi/gemmi) in these cases
