"""Implementations of algorithms for matching cycling data with various
models.


Models:

Power Duration Model: also known as Mean Max Power model or simply a power curve

Author: Maksym Sladkov
"""
from vmpy.utils import to_ndarray
from vmpy.preprocess import mask_filter
import numpy as np
import pandas as pd


def power_duration_curve(arg, mask=None, value=0.0, **kwargs):
    """Power-Duration Curve

    Compute power duration curve from the power stream. Mask-filter options can be
    added using the keyword arguments

    Parameters
    ----------
    arg : array-like
        Power stream
    mask: array-like, optional
        Replacement mask (the default is None, which implies no masking)
    value: number, optional
        Value to use as a replacement (the default is 0.0)

    Returns
    -------
    rv : type of input argument
        Power-Duration Curve
    """

    y_filtered = mask_filter(arg, mask=mask, value=value)

    y, arg_type = to_ndarray(y_filtered)

    ys = pd.Series(y)
    energy = ys.cumsum()
    rv = np.array([])
    for t in np.arange(1, len(energy)):
        rv = np.append(rv, energy.diff(t).max()/(t))

    if arg_type == list:
        rv = rv.tolist()

    return rv
