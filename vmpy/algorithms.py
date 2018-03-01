"""Implementations of algorithms for matching cycling data with various
models.


Models:

Power Duration Model: also known as Mean Max Power model or simply a power curve

Author: Maksym Sladkov
"""
from vmpy.preprocess import mask_fill
from vmpy.utils import cast_array_to_original_type
import numpy as np
import pandas as pd


def power_duration_curve(arg, mask=None, value=0.0, **kwargs):
    """Power-Duration Curve

    Compute power duration curve from the power stream. Mask-filter options can be
    added using the keyword arguments.

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

    y = mask_fill(arg, mask=mask, value=value)
    y = pd.Series(y)

    # Compute the accumulated energy from the power data
    energy = y.cumsum()

    # Compute the maximum sustainable power using the difference in energy
    # This method is x4 faster than using rolling mean
    y = np.array([])
    for t in np.arange(1, len(energy)):
        y = np.append(y, energy.diff(t).max()/(t))

    y = cast_array_to_original_type(y, type(arg))

    return y
