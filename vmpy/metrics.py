import numpy as np
import pandas as pd


def rolling_mean(stream, window, moving=None, **kwargs):
    """Rolling mean (default=10 sec) of the stream

    :param stream: array-like
    :param window: int, Size of the moving window in sec
    :param moving (optional): array-like of boolean to mark samples to use
    :return y: type of input argument

    The stream is expected to be sampled with 1 sec interval
    and is treated as a time series.

    The moving array will indicate which samples to set to zero before
    applying rolling mean.
    """

    # Infer stream data type and cast to dnarray
    _stream_type = type(stream)
    if _stream_type == list:
        _stream = np.asarray(stream)
    else:
        _stream = stream

    # Set all records with Moving=False to zero
    if moving is not None:
        if type(moving) == list:
            _moving = np.asarray(moving, dtype=bool)
        else:
            _moving = moving
    else:
        _moving = np.ones(_stream.size, dtype=bool)

    _stream[~_moving] = 0

    # Moving average using pandas rolling_mean
    _s = pd.Series(_stream)
    y = _s.rolling(window, min_periods=1).mean().values

    # Cast the result into original type
    if _stream_type == list:
        y = y.tolist()

    return y


#
# def getActivityId(self, activity):
#     activityId = activity.activity_id
#     return activityId
#
#
# def getActivityName(self, activity):
#     activityName = activity.activity_dict['name']
#     return activityName
#
#
# def getFTP(self, athlete):
#     FTP = float(athlete.current_athlete_dict['ftp'])
#     return FTP
#
#
# def getCP(self):
#     # TODO: Change definition of CP
#     CP = self.FTP
#     return CP
#
#
# def getDuration(self, activity):
#     duration = activity.activity_dict['moving_time']
#     return duration
#
#
# def calc_nWorkCP(self):
#     nWorkCP = self.CP * 3600
#     return nWorkCP
#
#
# def calc_maxPower(self, activity):
#     return np.max(activity.watts)
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