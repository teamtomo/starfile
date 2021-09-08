from setuptools import setup
from starfile.version import __version__

setup(
    name='starfile',
    version=__version__,
    packages=['starfile'],
    url='https://github.com/alisterburt/starfile',
    license='BSD 3-Clause License',
    author='Alister Burt',
    author_email='alisterburt@gmail.com',
    description='STAR file reading and writing in python',
    python_requires='>=3.7',
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
