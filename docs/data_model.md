# Data Model

## File Model

STAR files are modelled as dictionaries where the keys are strings and the values are data blocks.
(`dict[str, DataBlock]`) 

Data blocks are either a dictionary or a dataframe (see below).

## Simple Blocks

Simple blocks contain `key`, `value` pairs which are naturally exposed as dictionaries in Python.

```txt
data_general

_rlnFinalResolution                        16.363636
_rlnBfactorUsedForSharpening                0.000000
_rlnUnfilteredMapHalf1                  average_symmetrized_ref_001_ite_0008.mrc
_rlnUnfilteredMapHalf2                  average_symmetrized_ref_002_ite_0008.mrc
_rlnMaskName                            mask.mrc
_rlnRandomiseFrom                          32.727273
```

```python
{
    'rlnFinalResolution': 16.363636,
    'rlnBfactorUsedForSharpening': 0.0,
    'rlnUnfilteredMapHalf1': 'average_symmetrized_ref_001_ite_0008.mrc',
    'rlnUnfilteredMapHalf2': 'average_symmetrized_ref_002_ite_0008.mrc',
    'rlnMaskName': 'mask.mrc',
    'rlnRandomiseFrom': 32.727273
}

```

For more information about working with dictionaries in Python check out 
[this guide](https://www.codecademy.com/learn/learn-python-3/modules/learn-python3-dictionaries/cheatsheet).


## Loop Blocks

Loop blocks contain tabular data and are which are naturally exposed as pandas dataframes.

```txt
data_fsc

loop_ 
_rlnSpectralIndex #1 
_rlnResolution #2 
_rlnAngstromResolution #3 
_rlnFourierShellCorrelationCorrected #4 
_rlnFourierShellCorrelationUnmaskedMaps #5 
_rlnFourierShellCorrelationMaskedMaps #6 
_rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps #7 
           0     0.001001   999.000000     1.000000     1.000000     1.000000     1.000000 
           1     0.001389   720.000000     0.999943     0.999883     0.999943     0.999964 
           2     0.002778   360.000000     0.999902     0.998804     0.999902     0.999856 
...
          47     0.065278    15.319149     0.240980     0.055721     0.319111     0.102936 
          48     0.066667    15.000000     0.282401     0.067334     0.371575     0.124267 
```

```ipython
Out[1]: 

<class 'pandas.core.frame.DataFrame'>
    rlnSpectralIndex  rlnResolution  ...  rlnFourierShellCorrelationMaskedMaps  rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps
0                  0       0.001001  ...                              1.000000                                           1.000000           
1                  1       0.001389  ...                              0.999943                                           0.999964           
2                  2       0.002778  ...                              0.999902                                           0.999856           
...
47                47       0.065278  ...                              0.319111                                           0.102936           
48                48       0.066667  ...                              0.371575                                           0.124267     
[49 rows x 7 columns]

```