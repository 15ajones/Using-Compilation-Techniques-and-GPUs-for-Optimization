from distutils.core import setup
from Cython.Build import cythonize
import numpy
from time import time
setup(ext_modules=cythonize("cythonfn.pyx", compiler_directives={"language_level":"3"}))

# python3 setup.py build_ext --inplace