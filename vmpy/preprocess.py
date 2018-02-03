"""Implementation of help functions for data preprocessing
Author: Maksym Sladkov"""

import numpy as np
import pandas as pd


def sanitize_stream(stream, mask=None, **kwargs):
    """Fill mask=False with default=0 or specified by value

    :param stream: array-like
    :param mask (optional): array-like of bools
    :param value (optional): value to use to fill moving=False, default=0.0
    """

    # Infer stream data type and cast to dnarray
    _stream_type = type(stream)
    if _stream_type == list:
        _stream = np.asarray(stream)
    else:
        _stream = stream

    if mask is not None:
        if type(mask) == list:
            _mask = np.asarray(mask, dtype=bool)
        else:
            _mask = mask
    else:
        _mask = np.ones(_stream.size, dtype=bool)

    _stream[~_mask] = kwargs.get('value', 0.0)

    return _stream


def rolling_mean(stream, window, mask=None, **kwargs):
    """Rolling mean (default=10 sec) of the stream

    :param stream: array-like
    :param window: int, Size of the moving window in sec
    :param mask (optional): array-like of boolean to mark samples to use
    :param value (optional): Value to use to fill mask=False, default=0.0
    :param type (optional): str, type of averaging default="uniform", "ewma",
    window is used as a span
    :return y: type of input argument

    The stream is expected to be sampled with 1 sec interval
    and is treated as a time series.

    The moving array will indicate which samples to set to zero before
    applying rolling mean.
    """

    # Set all records with Moving=False to zero
    _stream = sanitize_stream(stream, mask, **kwargs)

    # Moving average using pandas rolling_mean
    _s = pd.Series(_stream)

    if kwargs.get('type', 'uniform') == 'ewma':
        y = _s.ewm(span=window, min_periods=1).mean().values
    else:
        y = _s.rolling(window, min_periods=1).mean().values

    # Cast the result into original type
    if type(stream) == list:
        y = y.tolist()

    return y


def hampel_filter(stream, window=11, threshold=3, **kwargs):
    """Detect outliers using Hampel filter and replace with rolling median or specified value

    :param stream: array-like
    :param window int: default=11, size of window (including the sample; 11 is equal to 5 on either side of value)
    :param threshold float: default=3 and corresponds to 3xSigma
    :param value float: default=None, will be replaced by rolling median value
    :return y: type of input argument

    The factor 1.4826 makes the MAD scale estimate
    an unbiased estimate of the standard deviation for Gaussian data.
    """

    if type(stream) == np.ndarray:
        _stream = stream.copy()
    else:
        _stream = np.array(stream)

    y = pd.Series(_stream)

    #Hampel Filter

    rolling_median = y.rolling(window, min_periods=1).median()

    difference = np.abs(y - rolling_median)
    median_abs_deviation = difference.rolling(window, min_periods=1).median()

    outlier_idx = difference > 1.4826 * threshold * median_abs_deviation

    y[outlier_idx] = rolling_median[outlier_idx]

    if type(stream) == list:
        y = y.tolist()

    return y
