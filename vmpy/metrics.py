import numpy as np
import pandas as pd


def rolling_mean(stream, window, moving=None, **kwargs):
    """Rolling mean (default=10 sec) of the stream

    :param stream: array-like
    :param window: int, Size of the moving window in sec
    :param moving (optional): array-like of boolean to mark samples to use
    :param value (optional): Value to use to fill moving=False, default=0.0
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
    y = _s.rolling(window, min_periods=1).mean().values

    # Cast the result into original type
    if type(stream) == list:
        y = y.tolist()

    return y


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

#
#
# def calc_avPower(self, activity):
#     avPower = np.mean(activity.power3)
#     return avPower
#
#
# def calc_medPower(self, activity):
#     return np.median(activity.watts)
#
#
# def calc_xPower(self, activity):
#     power = activity.power_ewma25
#     xPower = np.mean(np.power(power, 4)) ** (1.0 / 4)
#     return xPower
#
#
# def calc_nPower(self, activity):
#     power = activity.power30
#     nPower = np.mean(np.power(power, 4)) ** (1.0 / 4)
#     return nPower
#
#
# def calc_relIntensity(self):
#     relIntensity = self.xPower / self.CP
#     return relIntensity
#
#
# def calc_nWorkSession(self):
#     nWorkSession = self.xPower * self.duration
#     return nWorkSession
#
#
# def calc_IF(self):
#     IF = self.nPower / self.FTP
#     return IF
#
#
# def calc_rawBikeScore(self):
#     rawBikeScore = self.relIntensity * self.nWorkSession
#     return rawBikeScore
#
#
# def calc_bikeScore(self):
#     bikeScore = self.rawBikeScore / self.nWorkCP * 100
#     return bikeScore
#
#
# def calc_TSS(self):
#     TSS = (self.duration * self.nPower * self.IF) / (self.FTP * 3600) * 100
#     return TSS
#
#
# def calc_avSpeed(self, activity):
#     return np.mean(activity.speed)
#
#
# def calc_maxSpeed(self, activity):
#     return np.max(activity.speed)
#
#
# def calc_medSpeed(self, activity):
#     return np.median(activity.speed)
#
#
# def calc_maxBPM(self, activity):
#     return np.max(activity.heartrate)
#
#
# def calc_avBPM(self, activity):
#     return np.mean(activity.heartrate)
#
#
# def calc_medBPM(self, activity):
#     return np.median(activity.heartrate)
#
# def calc_PowerZones(self):
#     ZLIMITS = np.array([0.56, 0.76, 0.91, 1.06, 1.21, 1.51])
#     return ZLIMITS*self.FTP