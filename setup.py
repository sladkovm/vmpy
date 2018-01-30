from distutils.core import setup

setup(
    name='VmPy',
    version='0.1.0',
    author='Maksym Sladkov',
    author_email='sladkovm@gmail.com',
    packages=['vmpy'],
    url='http://pypi.python.org/pypi/VmPy/',
    license='LICENSE.txt',
    description='Velo Metrics implemented Python',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "json"
    ],
)