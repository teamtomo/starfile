from distutils.core import setup
from starfile.version import VERSION
setup(
  name = 'starfile',         # How you named your package folder (MyLib)
  packages = ['starfile'],   # Chose the same as "name"
  version = f'{VERSION}',      # Start with a small number and increase it with every change you make
  license='BSD 3-Clause License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Read and write STAR files as pandas DataFrames',   # Give a short description about your library
  author = 'AlisterBurt',                   # Type in your name
  author_email = 'alisterburt@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/alisterburt/starfile',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['io', 'STAR'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'openpyxl',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD 3-Clause License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)