import os
from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'numpy',
    'pandas',
    'logging',
    'dateutils',
    'matplotlib>=1.5',
    'mlpy'
    ]

tests_require = [
    'mock',
    'nose',
    ]

setup(name='velometria',
      version='0.1',
      description='velometria',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite="nose.collector",
      )