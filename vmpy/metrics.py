import numpy as np
from vmpy.preprocess import rolling_mean


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