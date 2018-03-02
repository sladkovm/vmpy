Changelog
=========

0.X.X (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- Stress in zone

Bug fixes:

- *add item here*


0.1.7 (in progress)
------------------

Breaking changes:

- *add item here*

New features:

- Stress in zone

Bug fixes:

- *add item here*


0.1.6 (2018-03-02)
------------------

Breaking changes:

- All stream shape preserving metrics did move to streams.py
- All other calculations did move to metrics.py

New features:

- NumPy Style Python Docstrings
  (https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
- Power Duration Curve
- WPK calculations on array-like
- Time in zone

Bug fixes:

- *add item here*


0.1.5 (2018-02-11)
------------------

Breaking changes:

- all preprocess functions are working on the reference to the ndarray.
  If one wants to work with a copy it must be created explicitly outside of the functions

New features:

- Humpel filter (rolling median with median replacement) for outlier replacements
- Power and Heart Rate zones