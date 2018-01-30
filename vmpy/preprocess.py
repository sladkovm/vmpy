"""Implementation of help functions for data preprocessing
Author: Maksym Sladkov"""

import numpy as np
import pandas as pd


def sanitize_stream(stream, moving=None, **kwargs):
    """Fill moving=False and remove outliers

    :param stream: array-like
    :param moving (optional): array-like of bools
    :param value (optional): value to use to fill moving=False, default=0.0
    """

    # Infer stream data type and cast to dnarray
    _stream_type = type(stream)
    if _stream_type == list:
        _stream = np.asarray(stream)
    else:
        _stream = stream

    if moving is not None:
        if type(moving) == list:
            _moving = np.asarray(moving, dtype=bool)
        else:
            _moving = moving
    else:
        _moving = np.ones(_stream.size, dtype=bool)

    _stream[~_moving] = kwargs.get('value', 0.0)

    return _stream


def rolling_mean(stream, window, moving=None, **kwargs):
    """Rolling mean (default=10 sec) of the stream

    :param stream: array-like
    :param window: int, Size of the moving window in sec
    :param moving (optional): array-like of boolean to mark samples to use
    :param value (optional): Value to use to fill moving=False, default=0.0
    :param type (optional): str, type of averaging default="uniform", "ewma",
    window is used as a span
    :return y: type of input argument

    The stream is expected to be sampled with 1 sec interval
    and is treated as a time series.

    The moving array will indicate which samples to set to zero before
    applying rolling mean.
    """

    # Set all records with Moving=False to zero
    _stream = sanitize_stream(stream, moving, **kwargs)

    # Moving average using pandas rolling_mean
    _s = pd.Series(_stream)

    if kwargs.get('type', 'uniform') == 'emwa':
        y = _s.ewm(span=window, min_periods=1).mean().values
    else:
        y = _s.rolling(window, min_periods=1).mean().values

    # Cast the result into original type
    if type(stream) == list:
        y = y.tolist()

    return y