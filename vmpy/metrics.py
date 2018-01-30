"""Implementation of Cycling Performance Metrics
Author: Maksym Sladkov
"""

import numpy as np
from vmpy.preprocess import rolling_mean


POWER_ZONES_THRESHOLD = [0.55, 0.75, 0.90, 1.05, 1.20, 1.50]


def best_interval(stream, window, moving=None, **kwargs):
    """Calculate best interval of the stream

    :param stream: array-like
    :param window: int, duration of the interval in seconds
    :return best_interval: float
    """

    _stream = rolling_mean(stream, window=window, moving=moving, **kwargs)

    if type(_stream) == list:
        _stream = np.asarray(_stream)

    rv = _stream.max()

    return rv


def normalized_power(stream, moving=None, **kwargs):
    """Normalized power

    :param stream: array-like power stream
    :param moving (optional): array-like moving bools
    :param type (optional): str, default='NP', "xPower"
    """

    if kwargs.get('type', 'NP') == 'xPower':
        _rolling_mean = rolling_mean(stream, window=25, moving=moving, type='emwa')
    else:
        _rolling_mean = rolling_mean(stream, window=30, moving=moving)

    if type(_rolling_mean) == list:
        _rolling_mean = np.asarray(_rolling_mean, dtype=np.float)

    rv = np.mean(np.power(_rolling_mean, 4)) ** (1.0 / 4)

    return rv


def relative_intensity(norm_power, threshold_power):
    """Relative intensity

    :param norm_power: NP or xPower
    :param threshold_power: FTP or CP
    :return float: IF or RI
    """

    return norm_power/threshold_power


def stress_score(norm_power, threshold_power, duration):
    """Stress Score

    :param norm_power: NP or xPower
    :param threshold_power: FTP or CP
    :param duration: in seconds
    :return ss: TSS or BikeScore
    """

    ri = relative_intensity(norm_power, threshold_power)

    ss = (duration * norm_power * ri) \
         / (threshold_power * 3600) * 100

    return ss
