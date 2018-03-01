"""Implementation of help functions for data preprocessing
Author: Maksym Sladkov"""

import numpy as np
import pandas as pd
from vmpy.utils import to_ndarray


def mask_filter(arg, mask, value=0.0, **kwargs):
    """Replace masked values

    :param arg: array-like
    :param mask: array-like of bools
    :param value: value to use for replacement, default=0.0
    :return y: type of input argument

    In case the arg is an ndarray all operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """

    if mask is None:
        return arg

    y, arg_type = to_ndarray(arg)

    if type(mask) == list:
        ndmask = np.asarray(mask, dtype=bool)
    else:
        ndmask = mask

    y[~ndmask] = value

    if arg_type == list:
        y = y.tolist()

    return y


def hampel_filter(arg, window=31, threshold=1, value=None, **kwargs):
    """Detect outliers using Hampel filter and replace with rolling median or specified value

    :param arg: array-like
    :param window int: default=11, size of window (including the sample; 31 is equal to 15 on either side of value)
    :param threshold float: default=3 and corresponds to 2xSigma
    :param value float: if left to default=None, will be replaced by rolling median value
    :return y: type of input argument

    The factor 1.4826 makes the MAD scale estimate
    an unbiased estimate of the standard deviation for Gaussian data.

    In case the arg is an ndarray all operations will be performed on the original array.
    To preserve original array pass a copy to the function
    """

    y, arg_type = to_ndarray(arg)

    y_stream = pd.Series(y)

    rolling_median = y_stream.rolling(window, min_periods=1).median()

    difference = np.abs(y_stream - rolling_median)

    median_abs_deviation = difference.rolling(window, min_periods=1).median()

    outlier_idx = difference > 1.4826 * threshold * median_abs_deviation

    if value:
        y_stream[outlier_idx] = value
    else:
        y_stream[outlier_idx] = rolling_median[outlier_idx]

    y = y_stream.as_matrix()

    if arg_type == list:
        y = y.tolist()

    return y


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

    y, type_stream = to_ndarray(stream)

    if mask is not None:

        y = mask_filter(y, mask, **kwargs)

    _s = pd.Series(y)

    if kwargs.get('type', 'uniform') == 'ewma':
        y = _s.ewm(span=window, min_periods=1).mean().values
    else:
        y = _s.rolling(window, min_periods=1).mean().values

    if type_stream == list:
        y = y.tolist()

    return y

