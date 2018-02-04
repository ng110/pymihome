from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pymihome',
      version='0.1',
      description='Library to access Energenie MiHome devices via the web API.',
#      url='',
      author='Neil Griffin',
      author_email='ngriffin110@gmail.com',
      license='tbd',   # MIT, BSD
      packages=['pymihome'],
      long_description=read('README.md'),
#      keywords = ["photos"],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Topic :: Utilities",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
#          "License :: OSI Approved :: BSD GNU General Public License (GPL)",
          "Operating System :: OS Independent"],
      zip_safe=True
      )





# https://pypi.python.org/pypi?%3Aaction=list_classifiers
# # Development Status :: 1 - Planning
# Development Status :: 2 - Pre-Alpha
# Development Status :: 3 - Alpha
# Development Status :: 4 - Beta
# Development Status :: 5 - Production/Stable
# Development Status :: 6 - Mature
# Development Status :: 7 - Inactive
