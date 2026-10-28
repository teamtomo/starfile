"""
PEP 517 doesn't support editable installs
so this file is currently here to support "pip install -e ."
"""  # noqa: RUF002
from setuptools import setup

setup(
    use_scm_version={"write_to": "starfile/_version.py"},
    setup_requires=["setuptools_scm"],
)
