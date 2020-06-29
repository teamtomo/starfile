# Package up starfile for distribution
python setup.py sdist
twine upload dist/*