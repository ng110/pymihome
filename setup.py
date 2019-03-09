from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.6'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
# with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

# install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
install_requires = ['requests']
#dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]
dependency_links = []

setup(
    name='pymihome',
    version=__version__,
    description='Library to access Energenie MiHome devices via the web API.',
    long_description=long_description,
    author='Neil Griffin',
    author_email='ngriffin110@gmail.com',
    url='https://github.com/ng110/pymihome',
    download_url='https://github.com/ng110/pymihome/tarball/' + __version__,
    license='LGPLv3',
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Topic :: Utilities",
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
      "Operating System :: OS Independent",
      "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    keywords='energenie mihome',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links
)
