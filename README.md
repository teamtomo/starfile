# starfile

[![License](https://img.shields.io/pypi/l/starfile.svg?color=green)](https://github.com/teamtomo/starfile/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/starfile.svg?color=green)](https://pypi.org/project/starfile)
[![Python Version](https://img.shields.io/pypi/pyversions/starfile.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/starfile/actions/workflows/ci.yml/badge.svg)](https://github.com/teamtomo/starfile/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/teamtomo/starfile/branch/main/graph/badge.svg)](https://codecov.io/gh/teamtomo/starfile)


*starfile* is a Python package for [STAR](https://en.wikipedia.org/wiki/Self-defining_Text_Archive_and_Retrieval) 
file IO. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/7307488/204108873-c2175153-fb5b-4b22-892a-0a1274616057.png" width="400">
  <figcaption>reading and writing a STAR file with a single loop block.</figcaption>
</p>

*starfile* was designed principally for reading and writing of STAR files compatible with
[RELION](https://github.com/3dem/relion).

```
The STAR file: a new format for electronic dataframes transfer and archiving
J. Chem. Inf. Comput. Sci. 1991, 31, 2, 326–333
Publication Date: May 1, 1991
https://doi.org/10.1021/ci00002a020
```

## Installation

*starfile* can be installed from the [Python package index](https://pypi.org/project/starfile/)

```bash
pip install starfile
```

Currently `python` >= `3.8` is supported. You can check your `python` version with

```sh
python -V
```

We recommend working in a virtual environment.

## Quickstart

```python
import starfile

# data blocks are simple dictionaries or pandas dataframes
# reading a file returns a single data block or a dict of data blocks
data = starfile.read(file)

# single data blocks or dicts of data blocks can be written to disk
starfile.write(data, 'output.star')
```

## Usage

For more details please check out [teamtomo.org/starfile](https://teamtomo.org/starfile/).

## Known Issues
- Cannot handle more than one loop in a data block as found in mmCIF files, please use 
[GEMMI](https://github.com/project-gemmi/gemmi) in these cases.
