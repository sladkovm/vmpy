Changelog
=========

0.X.X (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- *add item here*


0.1.6 (in progress)
------------------

Breaking changes:

- NumPy Style Python Docstrings
  (https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)

New features:

- Power Duration Curve
- WPK calculations on array-like
- Time in zone (to-do)
- Stress in zone (to-do)

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