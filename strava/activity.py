import logging
import numpy as np
from pandas import ewma, rolling_mean, rolling_window
import athlete, streams, utilities, vmplotlib
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

class Activity():
    '''
    Activities are the base object for Strava runs, rides, swims etc.

    Call: test_activity = activity.Activity(activity_id)
          test_activity = activity.Activity(activity_id, _athlete)

          If parameter _athlete is not specified, it will be initialized based on the content
          of config/athlete.config file

    Inputs: activity_id [str] Ex. '227615'
            _athlete (optional) [athlete.Athlete] Ex. john_the_athlete = athlete.Athlete()

    Property methods: speed, watts, power3 ... will return filtered ndarray of streams with non-moving data excluded
                      ready for further numerical processing

    Plot methods:
        plot_strava_analysis_simple(title='Activity analysis'), title is optional
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
        _streams = streams.Streams(_activity_id, _athlete)
        return _streams

        # ------- End of Activity class --------------

    # ----- Getter functions -------

    @property
    def moving_slice(self):
        _moving = self.streams.streams_dict_np['moving']
        _moving_slice = np.where(_moving==True)
        return _moving_slice

    @property
    def watts(self):
        """Get the power stream"""
        if (self.streams.streams_dict_np['watts']!=None):
            _watts = self.streams.streams_dict_np['watts'][self.moving_slice]
            _watts = np.nan_to_num(_watts)
        else:
            raise LookupError('No watts stream found in activity with id = %i', self.activity_id)
            _watts = NotImplemented
        return _watts

    @property
    def power10(self):
        """Get power averaged over 10 sec"""
        return rolling_mean(self.watts, 10)

    @property
    def power3(self):
        """Get power averaged over 3 sec"""
        return rolling_mean(self.watts, 3)

    @property
    def power_ewma25(self):
        """Get power emwa averaged over 25 sec"""
        return ewma(self.watts, 25)

    @property
    def distance(self):
        """Get distance in km"""
        return self.streams.streams_dict_np['distance'][self.moving_slice]*1e-3

    @property
    def altitude(self):
        """Get altitude in m"""
        return self.streams.streams_dict_np['altitude'][self.moving_slice]

    @property
    def heartrate(self):
        """Get heartrate in bpm"""
        return self.streams.streams_dict_np['heartrate'][self.moving_slice]

    @property
    def cadence(self):
        """Get cadence in rpm"""
        return self.streams.streams_dict_np['cadence'][self.moving_slice]

    @property
    def time(self):
        """Get time in sec"""
        return self.streams.streams_dict_np['time'][self.moving_slice]

    @property
    def speed(self):
        """Get speed in km/h"""
        return self.streams.streams_dict_np['velocity_smooth'][self.moving_slice]*3600*1e-3

    @property
    def latlng(self):
        """Get lating"""
        return self.streams.streams_dict_np['latlng'][self.moving_slice]

    # --- Plot functions ---

    def plot_strava_analysis_simple(self, **kwargs):
        """Plot Strava-like analysis plot for this activity"""
        _title = kwargs.get('title', 'Strava analysis plot')
        vmplotlib.SimpleStravaPlot.plot_strava_analysis_simple(self, title=_title)

# ====== Compare Activities class ============

class CompareActivities(object):

    def __init__(self, activity1, activity2):
        self.activity1 = activity1
        self.activity2 = activity2
        self.syncronized_power_streams = None # Tuple place holder for activities power streams synchronized by shift

    def plot_compare_power_streams(self, **kwargs):
        """plot two power profiles as a function of index"""
        _shift = kwargs.get('shift', 0)
        _labels = kwargs.get('labels', ['activity1', 'activity2'])
        activity1 = self.activity1
        activity2 = self.activity2
        s1 = len(activity1.power_ewma25)
        s2 = len(activity2.power_ewma25)
        x1 = np.arange(s1)
        x2 = np.arange(s2)
        # plot part
        plt.style.use('ggplot')
        f, ax = plt.subplots(1)
        ax = plt.plot(x1, activity1.power_ewma25)
        plt.hold(True)
        ax = plt.plot(x2 + _shift, activity2.power_ewma25, 'blue')
        plt.xlabel('Index')
        plt.ylabel('Power')
        plt.legend(_labels)
        plt.show()
        return (f, ax)

    def synchronize_activities_by_power_shifting(self, **kwargs):
        """Syncronize two activities according to shift alement and return common distance vector and two power vectors"""
        shift = kwargs.get('shift', 0)
        is_plot = kwargs.get('is_plot', True)
        is_remove_negative = kwargs.get('is_remove_negative', False)
        activity1 = self.activity1
        activity2 = self.activity2
        distance1 = activity1.distance
        power1 = activity1.power_ewma25
        distance2 = activity2.distance
        power2 = activity2.power_ewma25
        # synchronize distance vectors between activities 1 and 2
        distance2_shift = distance2 + distance1[shift]
        # interpolate power of second activity to vector of distance one
        power2_interp = np.interp(distance1, distance2_shift, power2, left=0.0, right=0.0)
        # Find zero power elements in the power2 and set according elements to zero in the power1
        idx_zero = np.where(power2_interp < 1e-6)
        power1[idx_zero] = 0.0
        # Preoare and return variables
        syncronized_power_streams = {'distance':distance1, 'power1':power1, 'power2':power2_interp, 'shift':shift}
        self.syncronized_power_streams = syncronized_power_streams
        if is_plot:
            self._plot_difference_power_profile(syncronized_power_streams['distance'],
                                                syncronized_power_streams['power1'],
                                                syncronized_power_streams['power2'],
                                                is_remove_negative=is_remove_negative)
        return syncronized_power_streams

    def _plot_difference_power_profile(self, distance, power1, power2, **kwargs):
        """Visualize difference in power profiles"""
        plt.style.use('ggplot')
        is_remove_negative = kwargs.get('is_remove_negative', False)
        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.fill_between(distance, power1, power2, where=power2 >= power1, facecolor='red', interpolate=True)
        ax1.fill_between(distance, power1, power2, where=power2 < power1, facecolor='blue', interpolate=True)
        ax1.plot(distance, power1, color='grey')
        ax1.plot(distance, power2, color='grey')
        ax1.set_ylabel('Power [Watts]')
        ax1.set_title('Power profiles overlap')
        power_diff = power2 - power1
        if is_remove_negative:
            neg_idx = np.where(power_diff <= 0.0)  # find negative values
            power_diff[neg_idx] = 0.0  # set negative values to zero
        ax2.plot(distance, power_diff)
        ax2.set_ylabel('Power [Watts]')
        ax2.set_xlabel('Distance [km]')
        ax2.set_title('Power difference')
        plt.show()
        return (f, ax1, ax2)


class ActivityMetrics(object):
    """Integrated metrics based on activity stream and athlete parameters

    Args:
        athlete  [Athlete] : Athlete profile object that contains, ex: FTP, FTHR, weight etc...
        activity [Activity]: Activity object that includes activity streams

    Attributes:
       ...
    """
    def __init__(self, activity, athlete):
        self.activity_id = self.getActivityId(activity)
        self.activityName = self.getActivityName(activity)
        self.FTP = self.getFTP(athlete)
        self.CP = self.getCP()
        self.duration = self.getDuration(activity)
        self.nWorkCP = self.calc_nWorkCP()
        self.avPower = self.calc_avPower(activity)
        self.xPower = self.calc_xPower(activity)
        self.nPower = self.calc_nPower(activity)
        self.relIntensity = self.calc_relIntensity()
        self.IF = self.calc_IF()
        self.nWorkSession = self.calc_nWorkSession()
        self.rawBikeScore = self.calc_rawBikeScore()
        self.bikeScore = self.calc_bikeScore()
        self.TSS = self.calc_TSS()
        self.powerZones = self.calc_PowerZones()

    def getActivityId(self, activity):
        activityId = activity.activity_id
        return activityId

    def getActivityName(self, activity):
        activityName = activity.activity_dict['name']
        return activityName

    def getFTP(self, athlete):
        FTP = float(athlete.current_athlete_dict['ftp'])
        return FTP

    def getCP(self):
        # TODO: Change definition of CP
        CP = self.FTP
        return CP

    def getDuration(self, activity):
        duration = activity.activity_dict['moving_time']
        return duration

    def calc_nWorkCP(self):
        nWorkCP = self.CP * 3600
        return nWorkCP

    def calc_avPower(self, activity):
        avPower = np.mean(activity.streams.streams_dict_np['watts'])
        return avPower

    def calc_xPower(self, activity):
        ewmaSpan = 25 # in seconds
        power = activity.streams.streams_dict_np['watts']
        ewmaPower = ewma(power, span=ewmaSpan)
        xPower = np.mean(np.power(ewmaPower, 4))**(1.0/4)
        return xPower

    def calc_nPower(self, activity):
        CONV_LEN    = 30 # averaging over 30 sec
        CONV_FILT   = np.ones(CONV_LEN)
        power = activity.streams.streams_dict_np['watts']
        convPower = np.convolve(power, CONV_FILT, mode='same')/CONV_LEN
        nPower = np.mean(np.power(convPower, 4))**(1.0/4)
        return nPower

    def calc_relIntensity(self):
        relIntensity = self.xPower/self.CP
        return relIntensity

    def calc_nWorkSession(self):
        nWorkSession = self.xPower * self.duration
        return nWorkSession

    def calc_IF(self):
        IF = self.nPower/self.FTP
        return IF

    def calc_rawBikeScore(self):
        rawBikeScore = self.relIntensity * self.nWorkSession
        return rawBikeScore

    def calc_bikeScore(self):
        bikeScore = self.rawBikeScore/self.nWorkCP * 100
        return bikeScore

    def calc_TSS(self):
        TSS = (self.duration * self.nPower * self.IF)/(self.FTP*3600)*100
        return TSS

    def printMetrics(self):
        print '\n'
        print 'Activity: %s' %(self.name)
        print 'IF = %f, IR = %f' %(self.IF, self.relIntensity)
        print 'TSS = %f, BikeScore = %f' %(self.TSS, self.bikeScore)

    def calc_PowerZones(self):
        ZLIMITS = np.array([0.56, 0.76, 0.91, 1.06, 1.21, 1.51])
        return ZLIMITS*self.FTP

    # ------- End of ActivityMetrics class --------------

if (__name__=='__main__'):
    test_activity_id = '628508858' # mdd30
    test_athlete = athlete.Athlete()
    test_activity = Activity(test_activity_id)
    test_activity_metrics = ActivityMetrics(test_activity, test_athlete)

