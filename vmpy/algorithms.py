"""Implementations of algorithms for matching cycling data with various
models.


Models:

Power Duration Model: also known as Mean Max Power model or simply a power curve

Author: Maksym Sladkov
"""
from vmpy.utils import to_ndarray
import numpy as np
import pandas as pd


def power_duration_curve(arg, **kwargs):
    """
    Returns a power-duration curve

    :param arg: array-like
    :return y: type of input argument

    """

    y, arg_type = to_ndarray(arg)

    ys = pd.Series(y)
    energy = ys.cumsum()

    rv = np.array([])

    for t in np.arange(1, len(energy)):
        rv = np.append(rv, energy.diff(t).max()/(t))

    if arg_type == list:
        rv = rv.tolist()

    return rv
