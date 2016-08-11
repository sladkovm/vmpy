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
        self.activity_metrics = ActivityMetrics(activity=self, athlete=self.athlete)

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
    def power30(self):
        """Get power averaged over 30 sec"""
        return np.convolve(self.watts, 30, mode='same')/30.0

    @property
    def power10(self):
        """Get power averaged over 10 sec"""
        return np.convolve(self.watts, 10, mode='same')/10.0

    @property
    def power3(self):
        """Get power averaged over 3 sec"""
        return np.convolve(self.watts, 3, mode='same')/3.0

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
        _is_show = kwargs.get('is_show', True)
        vmplotlib.SimpleStravaPlot(self, title=_title, is_show=_is_show)

# ====== Compare Activities class ============

class CompareActivities(object):
    def __init__(self, activity1, activity2):
        self.activity1 = activity1
        self.activity2 = activity2
        self.syncronized_power_streams = None  # Tuple place holder for activities power streams synchronized by shift

    def plot_all(self):
        t1 = self.activity1.time
        t2 = self.activity2.time
        d1 = self.activity1.distance
        d2 = self.activity2.distance
        f, axarr = plt.subplots(5, 2)
        # Plot latitude
        x1 = self.activity1.latlng[:, 0]
        x2 = self.activity2.latlng[:, 0]
        pn = 0
        self._plot_pannel(axarr, pn, x1, x2, 'lat')
        # Plot longitude
        x1 = self.activity1.latlng[:, 1]
        x2 = self.activity2.latlng[:, 1]
        pn = 1
        self._plot_pannel(axarr, pn, x1, x2, 'lng')
        # Plot speed
        x1 = self.activity1.speed
        x2 = self.activity2.speed
        pn = 2
        self._plot_pannel(axarr, pn, x1, x2, 'speed')
        # Plot power_ewma25
        x1 = self.activity1.power_ewma25
        x2 = self.activity2.power_ewma25
        pn = 3
        self._plot_pannel(axarr, pn, x1, x2, 'power_ewma25')
        # Plot bpm
        x1 = self.activity1.heartrate
        x2 = self.activity2.heartrate
        pn = 4
        self._plot_pannel(axarr, pn, x1, x2, 'bpm')

    def _plot_pannel(self, axarr, pn, x1, x2, ylabel):
        t1 = self.activity1.time
        t2 = self.activity2.time
        d1 = self.activity1.distance
        d2 = self.activity2.distance
        axarr[pn, 0].plot(t1, x1)
        axarr[pn, 0].plot(t2, x2, 'b')
        plt.setp(axarr[pn, 0], 'xlabel', 'time')
        plt.setp(axarr[pn, 0], 'ylabel', ylabel)
        axarr[pn, 1].plot(d1, x1)
        axarr[pn, 1].plot(d2, x2, 'b')
        plt.setp(axarr[pn, 1], 'xlabel', 'distance')

    def calc_com_distance_vector(self):
        d1 = self.activity1.distance
        d2 = self.activity2.distance
        l1 = len(d1)
        l2 = len(d2)
        d1_max = np.max(d1)
        d2_max = np.max(d2)
        com_d_max = np.max([d1_max, d2_max])
        com_d_l = 2 * np.max([l1, l2])  # oversample new distance vector
        com_distance_vector = np.linspace(0.0, com_d_max, num=com_d_l)
        return com_distance_vector

    def calc_resample_stream(self, xnew, xold, stream):
        resampled_stream = np.interp(xnew, xold, stream, left=-1.0, right=-1.0)
        return resampled_stream

    def plot_resampled_stream(self):
        d1 = self.activity1.distance
        d2 = self.activity2.distance
        p1 = self.activity1.power_ewma25
        p2 = self.activity2.power_ewma25
        d = self.calc_com_distance_vector()
        p1_new = self.calc_resample_stream(d, d1, p1)
        p2_new = self.calc_resample_stream(d, d2, p2)
        f, axarr = plt.subplots(2)
        axarr[0].plot(d, p1_new)
        axarr[0].plot(d, p2_new, color='b')
        axarr[1].plot(d, p2_new - p1_new)

    def calc_convolution_shift(self):
        x1 = self.activity1.latlng[:, 0]
        x2 = self.activity2.latlng[:, 0]
        conv = np.convolve(x1, x2, mode='same')
        shift = np.argmax(conv)

        f, (ax1, ax2) = plt.subplots(2)
        ax1.plot(x1)
        ax1.plot(x2, color='b')
        ax2.plot(conv)
        return shift

    def plot_compare_activities(self, **kwargs):
        title = kwargs.get('title', 'Compare activities')
        is_show = kwargs.get('is_show', False)
        compare_activities_plot = CompareActivitiesPlot(compare_activities=self, title=title, is_show=is_show)
        return compare_activities_plot

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
        syncronized_power_streams = {'distance': distance1, 'power1': power1, 'power2': power2_interp, 'shift': shift}
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


class CompareActivitiesPlot(object):
    def __init__(self, compare_activities, **kwargs):
        self.title = kwargs.get('title', 'Strava analysis plot')
        self.is_show = kwargs.get('is_show', True)
        self.compare_activities = compare_activities
        self.strava_plot = self.plot_compare_activities(title=self.title, is_show=self.is_show)  # tuple (f, axarr)

    def plot_compare_activities(self, **kwargs):
        """Line2D plots of velocity_smooth, power, heartrate"""
        _style = kwargs.get('style', 'ggplot')
        plt.style.use(_style)
        _title = kwargs.get('title', 'Strava analysis plot')
        _is_show = kwargs.get('is_show', True)

        # Init activities
        activity1 = self.compare_activities.activity1
        activity2 = self.compare_activities.activity2

        # Get common distance vector
        d_vec = self.compare_activities.calc_com_distance_vector()

        # Get streams
        d1 = activity1.distance
        d2 = activity2.distance
        conv_len = 60.0
        s1 = self._interp_and_convolve(d_vec, d1, activity1.speed, conv_len=conv_len)
        s2 = self._interp_and_convolve(d_vec, d2, activity2.speed, conv_len=conv_len)
        p1 = self._interp_and_convolve(d_vec, d1, activity1.power_ewma25, conv_len=conv_len)
        p2 = self._interp_and_convolve(d_vec, d2, activity2.power_ewma25, conv_len=conv_len)
        h1 = self._interp_and_convolve(d_vec, d1, activity1.heartrate, conv_len=conv_len)
        h2 = self._interp_and_convolve(d_vec, d2, activity2.heartrate, conv_len=conv_len)
        a1 = self._interp_and_convolve(d_vec, d1, activity1.altitude)
        a2 = self._interp_and_convolve(d_vec, d2, activity2.altitude)
        c1 = self._interp_and_convolve(d_vec, d1, activity1.cadence, conv_len=conv_len)
        c2 = self._interp_and_convolve(d_vec, d2, activity2.cadence, conv_len=conv_len)

        # Init plot canvas
        f, axarr = plt.subplots(3, sharex=True)
        # ax_bg = axarr

        # Add elevation background on each pannel
        for k, ax in enumerate(axarr):
            if (k == 0):
                ax_bg = self._add_elevation_background(ax, d_vec, a1, ylabel='Altitude [m]')
            else:
                ax_bg = self._add_elevation_background(ax, d_vec, a1)

        # Speed/Cadence plot
        ax_speed = axarr[0]

        ax_speed = self._add_line_plot(ax_speed, d_vec, s1, s2,
                                       ylabel=self._speed_labels(),
                                       title=_title)
        speed_labels_arr = self._calc_tick_labels(s1, s2)
        plt.setp(ax_speed, 'ylim', [speed_labels_arr[0], speed_labels_arr[-1]])
        plt.setp(ax_speed, 'yticks', speed_labels_arr[1:3])
        #
        # Power plot
        ax_power = axarr[1]
        ax_power = self._add_line_plot(ax_power, d_vec, p1, p2, ylabel=self._power_labels())
        power_labels_arr = self._calc_tick_labels(p1, p2, is_get_min=True)
        plt.setp(ax_power, 'ylim', [power_labels_arr[0], speed_labels_arr[-1]])
        plt.setp(ax_power, 'yticks', power_labels_arr[0:3])
        #
        # Heart Rate plot
        ax_heartrate = axarr[2]
        ax_heartrate = self._add_line_plot(ax_heartrate, d_vec, h1, h2,
                                           xlabel='Distance [km]',
                                           ylabel=self._bpm_labels())
        heartrate_labels_arr = self._calc_tick_labels(h1, h2, is_get_min=True)
        plt.setp(ax_heartrate, 'ylim', [heartrate_labels_arr[0], heartrate_labels_arr[-1]])
        plt.setp(ax_heartrate, 'yticks', heartrate_labels_arr[0:3])
        #
        # # f.subplots_adjust(hspace=0)
        # # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        if _is_show: plt.show()
        # return (f, axarr)

    def _interp_and_convolve(self, x_new, x_old, y_old, **kwargs):
        conv_len = kwargs.get('conv_len', 1.0)
        left = kwargs.get('left', -1.0)
        right = kwargs.get('right', -1.0)
        y_new = np.convolve(np.interp(x_new, x_old, y_old, left=left, right=right), conv_len) / conv_len
        return y_new

    def _speed_labels(self):
        act1 = self.compare_activities.activity1
        act2 = self.compare_activities.activity2
        max_s1 = act1.activity_metrics.maxSpeed
        avg_s1 = act1.activity_metrics.avSpeed
        med_s1 = act1.activity_metrics.medSpeed
        max_s2 = act2.activity_metrics.maxSpeed
        avg_s2 = act2.activity_metrics.avSpeed
        med_s2 = act2.activity_metrics.medSpeed
        speed_labels = '[km/h] \n' \
                       + 'Max {:02.0f} {:02.0f} \n'.format(max_s1, max_s2) \
                       + 'Avg {:02.0f} {:02.0f} \n'.format(avg_s1, avg_s2) \
                       + 'Med {:02.0f} {:02.0f} \n'.format(med_s1, med_s2)
        return speed_labels

    def _power_labels(self):
        act1 = self.compare_activities.activity1
        act2 = self.compare_activities.activity2
        max_p1 = act1.activity_metrics.maxPower
        avg_p1 = act1.activity_metrics.avPower
        np_p1 = act1.activity_metrics.nPower
        max_p2 = act2.activity_metrics.maxPower
        avg_p2 = act2.activity_metrics.avPower
        np_p2 = act2.activity_metrics.nPower
        power_labels = '[Watts] \n' \
                       + 'Max {:02.0f} {:02.0f} \n'.format(max_p1, max_p2) \
                       + 'Avg {:02.0f} {:02.0f} \n'.format(avg_p1, avg_p2) \
                       + 'NP {:02.0f} {:02.0f} \n'.format(np_p1, np_p2)
        return power_labels

    def _bpm_labels(self):
        act1 = self.compare_activities.activity1
        act2 = self.compare_activities.activity2
        max_h1 = act1.activity_metrics.maxBPM
        avg_h1 = act1.activity_metrics.avBPM
        med_h1 = act1.activity_metrics.medBPM
        max_h2 = act2.activity_metrics.maxBPM
        avg_h2 = act2.activity_metrics.avBPM
        med_h2 = act2.activity_metrics.medBPM
        bpm_labels = '[bpm] \n' \
                     + 'Max {:02.0f} {:02.0f} \n'.format(max_h1, max_h2) \
                     + 'Avg {:02.0f} {:02.0f} \n'.format(avg_h1, avg_h2) \
                     + 'Med {:02.0f} {:02.0f} \n'.format(med_h1, med_h2)
        return bpm_labels

    def _calc_tick_labels(self, stream1, stream2, **kwargs):
        is_get_min = kwargs.get('is_get_min', False)
        # Calc stream ranges
        y1 = stream1[np.where(stream1 >= 0.0)]
        y2 = stream1[np.where(stream2 >= 0.0)]
        min_stream = np.min([np.min(y1), np.min(y1)])
        max_stream = np.max([np.max(y2), np.max(y2)])
        # Calc stream ticks labels
        if is_get_min:
            min_stream_label = 10.0 * np.floor(min_stream / 10.0)
        else:
            min_stream_label = 0.0
        max_stream_label = 10.0 * np.ceil(max_stream / 10.0)
        mid_stream_label = (max_stream_label - min_stream_label) / 2.0 + min_stream_label
        return [min_stream_label, mid_stream_label, max_stream_label]

    def _add_line_plot(self, axes, x, y1, y2, **kwargs):
        xlabel = kwargs.get('xlabel', None)
        ylabel = kwargs.get('ylabel', None)
        title = kwargs.get('title', None)
        slice1 = np.where(y1 >= 0.0)
        slice2 = np.where(y2 >= 0.0)

        # Add fill_between
        com_slice = np.intersect1d(slice1[0], slice2[0])
        _x = x[com_slice]
        _y1 = y1[com_slice]
        _y2 = y2[com_slice]
        axes.fill_between(_x, _y1, _y2, where=_y1 >= _y2, facecolor='r', interpolate=True)
        axes.fill_between(_x, _y1, _y2, where=_y1 < _y2, facecolor='b', interpolate=True)

        # Add line plots
        axes.plot(x[slice1], y1[slice1], lw=0.25)
        axes.plot(x[slice2], y2[slice2], lw=0.25)

        # Add axes labels
        if xlabel is not None:
            axes.set_xlabel(xlabel)
        if ylabel is not None:
            axes.set_ylabel(ylabel, labelpad=40, rotation=0, y=1.0, verticalalignment='top')
        # Add title
        if title is not None:
            axes.set_title(title, horizontalalignment='right')
        return axes

    def _add_elevation_background(self, axes, x, y, **kwargs):
        """ Elevation profile background """
        ylabel = kwargs.get('ylabel', None)
        # Select valid points
        slice_y = np.where(y >= 0.0)
        _y = y[slice_y]
        _x = x[slice_y]
        # plot
        _ax = axes.twinx()
        _ax.fill_between(_x, np.ones(_y.shape) * np.min(_y), _y, facecolor='grey',
                         alpha=0.5,
                         linewidth=0.0)
        if ylabel is not None:
            _ax.set_ylabel(ylabel, rotation=0, y=1.3, horizontalalignment='right')
        _ax.gridOn = False
        alt_labels_arr = self._calc_tick_labels(_y, _y, is_get_min=True)
        plt.setp(_ax, 'ylim', [alt_labels_arr[0], alt_labels_arr[-1]])
        plt.setp(_ax, 'yticks', alt_labels_arr[0:3])
        return _ax

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
        self.maxPower = self.calc_maxPower(activity)
        self.avPower = self.calc_avPower(activity)
        self.medPower = self.calc_medPower(activity)
        self.xPower = self.calc_xPower(activity)
        self.nPower = self.calc_nPower(activity)
        self.relIntensity = self.calc_relIntensity()
        self.IF = self.calc_IF()
        self.nWorkSession = self.calc_nWorkSession()
        self.rawBikeScore = self.calc_rawBikeScore()
        self.bikeScore = self.calc_bikeScore()
        self.TSS = self.calc_TSS()
        self.powerZones = self.calc_PowerZones()
        self.avSpeed = self.calc_avSpeed(activity)
        self.medSpeed = self.calc_medSpeed(activity)
        self.maxSpeed = self.calc_maxSpeed(activity)
        self.maxBPM = self.calc_maxBPM(activity)
        self.avBPM = self.calc_avBPM(activity)
        self.medBPM = self.calc_medBPM(activity)

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

    def calc_maxPower(self, activity):
        return np.max(activity.watts)

    def calc_avPower(self, activity):
        avPower = np.mean(activity.power3)
        return avPower

    def calc_medPower(self, activity):
        return np.median(activity.watts)

    def calc_xPower(self, activity):
        power = activity.power_ewma25
        xPower = np.mean(np.power(power, 4))**(1.0/4)
        return xPower

    def calc_nPower(self, activity):
        power = activity.power30
        nPower = np.mean(np.power(power, 4))**(1.0/4)
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

    def calc_avSpeed(self, activity):
        return np.mean(activity.speed)

    def calc_maxSpeed(self, activity):
        return np.max(activity.speed)

    def calc_medSpeed(self, activity):
        return np.median(activity.speed)

    def calc_maxBPM(self, activity):
        return np.max(activity.heartrate)

    def calc_avBPM(self, activity):
        return np.mean(activity.heartrate)

    def calc_medBPM(self, activity):
        return np.median(activity.heartrate)

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
    # test_activity_id = '628508858' # mdd30
    # test_athlete = athlete.Athlete()
    # test_activity = Activity(test_activity_id)
    # test_activity_metrics = ActivityMetrics(test_activity, test_athlete)
    # test_activity.plot_strava_analysis_simple(title='#mdd30', is_show=True)

    # Test compare activities

    id_mdd28 = '163301368'
    id_mdd30 = '628508858'
    mdd28 = Activity(activity_id=id_mdd28)
    mdd30 = Activity(activity_id=id_mdd30)
    mdd_compare = CompareActivities(mdd30, mdd28)
    CompareActivitiesPlot(mdd_compare, title='#mdd30 vs #mdd28', is_show=True)