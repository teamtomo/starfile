from distutils.core import setup
from starfile.version import VERSION
setup(
  name = 'starfile',
  packages = ['starfile'],
  version = f'{VERSION}',
  license='BSD 3-Clause License',
  description = 'Read and write STAR files as pandas DataFrames',
  author = 'Alister Burt',
  author_email = 'alisterburt@gmail.com',
  url = 'https://github.com/alisterburt/starfile',
  download_url = 'https://github.com/alisterburt/starfile/archive/v0.1.tar.gz',
  keywords = ['io', 'STAR', 'star', 'starfile'],
  install_requires=[
          'pandas',
          'openpyxl',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)