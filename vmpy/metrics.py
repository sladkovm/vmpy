"""Implementation of Cycling Performance Metrics
Author: Maksym Sladkov
"""

import numpy as np
import pandas as pd
from vmpy.preprocess import rolling_mean
from vmpy.utils import to_ndarray
import logging
logger = logging.getLogger(__name__)

# left bin-edge + 7-zones
POWER_ZONES_THRESHOLD = [-0.001, 0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
POWER_ZONES_THRESHOLD_DESC = ["Active Recovery", "Endurance", "Tempo",
                              "Threshold", "VO2Max", "Anaerobic", "Neuromuscular",]
POWER_ZONES_THRESHOLD_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]

# left bin-edge + 5-zones
HEART_RATE_ZONES = [-0.001, 0.68, 0.83, 0.94, 1.05, 10.0]
HEART_RATE_ZONES_DESC = ["Active recovery", "Endurance", "Tempo", "Threshold", "VO2Max",]
HEART_RATE_ZONES_ZNAME = ["Z1", "Z2", "Z3", "Z4", "Z5"]


def best_interval(arg, window, mask=None, **kwargs):
    """Calculate best interval of the stream

    :param arg: array-like
    :param window: int, duration of the interval in seconds
    :param mask: array-like of bool
    :return rv: float
    """

    y = rolling_mean(arg, window=window, mask=mask, **kwargs)

    if type(y) == list:
        y = np.asarray(y)

    rv = y.max()

    return rv


def zones(arg, **kwargs):
    """Convert watts/hr stream into respective zones stream

    :param arg: array-like
    :keyword "ftp", "lthr" or "zones": list
    :return y: array-like, the same type as arg

    Depending on the provided keywords, different zone will be calculated:

    ftp: classic threshold based 7-zones
    lthr: classic heartrate based 5-zones
    zones: list of custom defined zones with left edge set to -1 and right edge to 10000
    """

    arg_ndarray, arg_type = to_ndarray(arg)

    arg_s = pd.Series(arg_ndarray)

    if kwargs.get('zones', None):
        abs_zones = kwargs.get('zones')
    elif kwargs.get('ftp', None):
        abs_zones = np.asarray(POWER_ZONES_THRESHOLD) * kwargs.get('ftp')
    elif kwargs.get('lthr', None):
        abs_zones = np.asarray(HEART_RATE_ZONES) * kwargs.get('lthr')
    else:
        raise ValueError

    labels = kwargs.get('labels', list(range(1, len(abs_zones))))
    assert len(abs_zones) == (len(labels) + 1)

    y = pd.cut(arg_s, bins=abs_zones, labels=labels)

    y = y.as_matrix()
    if arg_type == list:
        y = y.tolist()

    return y


def normalized_power(stream, mask=None, **kwargs):
    """Normalized power

    :param stream: array-like power stream
    :param moving (optional): array-like moving bools
    :param type (optional): str, default='NP', "xPower"
    """

    if kwargs.get('type', 'NP') == 'xPower':
        _rolling_mean = rolling_mean(stream, window=25, mask=mask, type='emwa')
    else:
        _rolling_mean = rolling_mean(stream, window=30, mask=mask)

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
