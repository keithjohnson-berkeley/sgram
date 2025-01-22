#!/usr/bin/env python

from distutils.core import setup

setup(
  name = 'sgram',
  version='0.2.1',
  py_modules = ['sgram'],
  classifiers = [
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Topic :: Multimedia :: Sound/Audio :: Speech'
  ],
  requires = [
    'scipy',
    'matplotlib'   
]

)
