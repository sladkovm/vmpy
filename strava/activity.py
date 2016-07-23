import logging, urllib2
import numpy as np
from pandas import ewma
import athlete, streams, utilities

logger = logging.getLogger(__name__)

class Activity():
    '''
    Activities are the base object for Strava runs, rides, swims etc.

    Call: test_activity = activity.Activity(activity_id)
          test_activity = activity.Activity(activity_id, _athlete)

    Inputs: activity_id [str]
            _athlete (optional) [athlete.Athlete]
    '''
    def __init__(self, activity_id, _athlete=None):
        self.activity_id = activity_id
        self.athlete = self._init_athlete(_athlete)
        self.activity_json = None
        self.activity_dict = None
        (self.activity_json, self.activity_dict) = self._retrieve_activity_summary()
        self.streams = self._retrieve_activity_streams()


    def _init_athlete(self, _athlete):
        if (_athlete==None):
            _athlete = athlete.Athlete()
        return _athlete

    def _retrieve_activity_summary(self, include_all_efforts=None):
        ''' https://strava.github.io/api/v3/athlete/'''
        _activity_id = self.activity_id
        _access_token = self.athlete.access_token
        logger.info('Retrieving an activity with id = %s', _activity_id)
        _url = 'https://www.strava.com/api/v3/activities/' + _activity_id
        _response = utilities.Utilities.strava_endpoint_request(_url, _access_token)
        _activity_json = _response
        _activity_dict = utilities.Utilities.json_to_dict(_response)
        return (_activity_json, _activity_dict)

    def _retrieve_activity_streams(self):
        _athlete = self.athlete
        _activity_id = self.activity_id
        _streams = streams.Streams(_athlete, _activity_id)
        return _streams

        # ------- End of Activity class --------------


# class ActivityMetrics(object):
#     """Integrated metrics based on activity stream and athlete parameters
#
#     Args:
#         athlete  [Athlete] : Athlete profile object that contains, ex: FTP, FTHR, weight etc...
#         activity [Activity]: Activity object that includes activity streams
#
#     Attributes:
#        ...
#     """
#     def __init__(self, athlete, activity):
#         self.id = self.getActivityId(activity)
#         self.name = self.getActivityName(activity)
#         self.FTP = self.getFTP(athlete)
#         self.CP = self.getCP()
#         self.duration = self.getDuration(activity)
#         self.nWorkCP = self.calc_nWorkCP()
#         self.avPower = self.calc_avPower(activity)
#         self.xPower = self.calc_xPower(activity)
#         self.nPower = self.calc_nPower(activity)
#         self.relIntensity = self.calc_relIntensity()
#         self.IF = self.calc_IF()
#         self.nWorkSession = self.calc_nWorkSession()
#         self.rawBikeScore = self.calc_rawBikeScore()
#         self.bikeScore = self.calc_bikeScore()
#         self.TSS = self.calc_TSS()
#         self.powerZones = self.calc_PowerZones()
#
#     def getActivityId(self, activity):
#         activityId = activity.activity_id
#         return activityId
#
#     def getActivityName(self, activity):
#         activityName = activity['name']
#         return activityName
#
#     def getFTP(self, athlete):
#         FTP = float(athlete.athleteDetails.ftp)
#         return FTP
#
#     def getCP(self):
#         # TODO: Change definition of CP
#         CP = self.FTP
#         return CP
#
#     def getDuration(self, activity):
#         duration = activity.activitySummary.moving_time.seconds
#         return duration
#
#     def calc_nWorkCP(self):
#         nWorkCP = self.CP * 3600
#         return nWorkCP
#
#     def calc_avPower(self, activity):
#         avPower = np.mean(activity.arrayStreams['watts'])
#         return avPower
#
#     def calc_xPower(self, activity):
#         ewmaSpan = 25 # in seconds
#         power = activity.arrayStreams['watts']
#         ewmaPower = ewma(power, span=ewmaSpan)
#         xPower = np.mean(np.power(ewmaPower, 4))**(1.0/4)
#         return xPower
#
#     def calc_nPower(self, activity):
#         CONV_LEN    = 30 # averaging over 30 sec
#         CONV_FILT   = np.ones(CONV_LEN)
#         power = activity.arrayStreams['watts']
#         convPower = np.convolve(power, CONV_FILT, mode='same')/CONV_LEN
#         nPower = np.mean(np.power(convPower, 4))**(1.0/4)
#         return nPower
#
#     def calc_relIntensity(self):
#         relIntensity = self.xPower/self.CP
#         return relIntensity
#
#     def calc_nWorkSession(self):
#         nWorkSession = self.xPower * self.duration
#         return nWorkSession
#
#     def calc_IF(self):
#         IF = self.nPower/self.FTP
#         return IF
#
#     def calc_rawBikeScore(self):
#         rawBikeScore = self.relIntensity * self.nWorkSession
#         return rawBikeScore
#
#     def calc_bikeScore(self):
#         bikeScore = self.rawBikeScore/self.nWorkCP * 100
#         return bikeScore
#
#     def calc_TSS(self):
#         TSS = (self.duration * self.nPower * self.IF)/(self.FTP*3600)*100
#         return TSS
#
#     def printMetrics(self):
#         print '\n'
#         print 'Activity: %s' %(self.name)
#         print 'IF = %f, IR = %f' %(self.IF, self.relIntensity)
#         print 'TSS = %f, BikeScore = %f' %(self.TSS, self.bikeScore)
#
#     def calc_PowerZones(self):
#         ZLIMITS = np.array([0.56, 0.76, 0.91, 1.06, 1.21, 1.51])
#         return ZLIMITS*self.FTP
#
    # ------- End of ActivityMetrics class --------------


if (__name__=='__main__'):
    test_activity_id = '628508858' # mdd30
    test_activity = Activity(test_activity_id)
    # test_activity_metrics = ActivityMetrics(athlete=test_athlete, activity=test_activity)

