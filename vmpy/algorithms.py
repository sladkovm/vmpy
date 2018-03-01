"""Implementations of algorithms for matching cycling data with various
models.


Models:

Power Duration Model: also known as Mean Max Power model or simply a power curve

Author: Maksym Sladkov
"""
from vmpy.preprocess import mask_fill
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

    y_filtered = mask_fill(arg, mask=mask, value=value)
    ys = pd.Series(y_filtered)

    energy = ys.cumsum()
    rv = np.array([])
    for t in np.arange(1, len(energy)):
        rv = np.append(rv, energy.diff(t).max()/(t))

    # Cast to original type
    arg_type = type(arg)
    if arg_type == list:
        rv = list(rv)

    elif arg_type == np.ndarray:
        rv = np.array(rv)

    elif arg_type == pd.Series:
        rv = pd.Series(rv)

    else:
        raise ValueError("arg_type must be list, ndarray or pd.Series")

    return rv
