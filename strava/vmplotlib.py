import numpy as np
from matplotlib import pyplot as plt

from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm


class SimpleStravaPlot(object):
    def __init__(self, activity, **kwargs):
        self.title = kwargs.get('title', 'Strava analysis plot')
        self.is_show = kwargs.get('is_show', True)
        self.activity = activity
        self.strava_plot = self.plot_strava_analysis_simple(title=self.title, is_show=self.is_show)  # tuple (f, axarr)

    def plot_strava_analysis_simple(self, **kwargs):
        """Line2D plots of velocity_smooth, power, heartrate"""
        _style = kwargs.get('style', 'ggplot')
        plt.style.use(_style)
        _title = kwargs.get('title', 'Strava analysis plot')
        _is_show = kwargs.get('is_show', True)

        activity = self.activity

        _distance = activity.distance
        _speed = activity.speed
        _power = activity.power_ewma25
        _heartrate = activity.heartrate
        _altitude = activity.altitude
        _cadence = activity.cadence

        f, axarr = plt.subplots(3, sharex=True)

        # Speed/Cadence plot
        ax_speed = axarr[0]
        ax_speed_bg = self._add_elevation_background(ax_speed, _distance, _altitude,
                                                     ylabel='Altitude [m]')
        _speedLabel = '[km/h] \n' \
                      + 'Max {:02.0f} \n'.format(activity.activity_metrics.maxSpeed) \
                      + 'Avg {:02.0f} \n'.format(activity.activity_metrics.avSpeed) \
                      + 'Med {:02.0f} \n'.format(activity.activity_metrics.medSpeed)
        ax_speed = self._add_line_plot(ax_speed, _distance, _speed,
                                       ylabel=_speedLabel, title=_title)
        speed_labels_arr = self._calc_tick_labels(_speed)
        plt.setp(ax_speed, 'ylim', [speed_labels_arr[0], speed_labels_arr[-1]])
        plt.setp(ax_speed, 'yticks', speed_labels_arr[1:3])

        # Power plot
        ax_power = axarr[1]
        ax_speed_bg = self._add_elevation_background(ax_power, _distance, _altitude)
        _powerLabel = '[Watts] \n' \
                      + 'Max {:03.0f} \n'.format(activity.activity_metrics.maxPower) \
                      + 'Avg {:03.0f} \n'.format(activity.activity_metrics.avPower) \
                      + 'NP {:03.0f}'.format(activity.activity_metrics.nPower)
        ax_power = self._add_line_plot(ax_power, _distance, _power, ylabel=_powerLabel)
        power_labels_arr = self._calc_tick_labels(_power, is_get_min=True)
        plt.setp(ax_power, 'ylim', [power_labels_arr[0], speed_labels_arr[-1]])
        plt.setp(ax_power, 'yticks', power_labels_arr[0:3])

        # Heart Rate plot
        ax_heartrate = axarr[2]
        ax_speed_bg = self._add_elevation_background(ax_heartrate, _distance, _altitude)
        _heartrateLabel = '[bpm] \n' \
                          + 'Max {:03.0f} \n'.format(activity.activity_metrics.maxBPM) \
                          + 'Avg {:03.0f} \n'.format(activity.activity_metrics.avBPM) \
                          + 'Med {:03.0f} \n'.format(activity.activity_metrics.medBPM)
        ax_heartrate = self._add_line_plot(ax_heartrate, _distance, _heartrate,
                                           xlabel='Distance [km]',
                                           ylabel=_heartrateLabel)
        heartrate_labels_arr = self._calc_tick_labels(_heartrate, is_get_min=True)
        plt.setp(ax_heartrate, 'ylim', [heartrate_labels_arr[0], heartrate_labels_arr[-1]])
        plt.setp(ax_heartrate, 'yticks', heartrate_labels_arr[0:3])

        # f.subplots_adjust(hspace=0)
        # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        if _is_show: plt.show()
        return (f, axarr)

    def _calc_tick_labels(self, stream, **kwargs):
        is_get_min = kwargs.get('is_get_min', False)
        # Calc stream ranges
        min_stream = np.min(stream)
        max_stream = np.max(stream)
        # Calc stream ticks labels
        if is_get_min:
            min_stream_label = 10.0 * np.floor(min_stream / 10.0)
        else:
            min_stream_label = 0.0

        max_stream_label = 10.0 * np.ceil(max_stream / 10.0)
        mid_stream_label = (max_stream_label - min_stream_label) / 2.0 + min_stream_label
        return [min_stream_label, mid_stream_label, max_stream_label]

    def _add_line_plot(self, axes, x, y, **kwargs):
        xlabel = kwargs.get('xlabel', None)
        ylabel = kwargs.get('ylabel', None)
        title = kwargs.get('title', None)
        axes.plot(x, y)
        if xlabel is not None:
            axes.set_xlabel(xlabel)
        if ylabel is not None:
            axes.set_ylabel(ylabel, labelpad=40, rotation=0, y=1.0, verticalalignment='top')
        if title is not None:
            axes.set_title(title, horizontalalignment='right')
        return axes

    def _add_elevation_background(self, axes, x, y, **kwargs):
        """ Elevation profile background """
        ylabel = kwargs.get('ylabel', None)
        _ax = axes.twinx()
        _ax.fill_between(x, np.ones(y.shape) * np.min(y), y, facecolor='grey',
                         alpha=0.5,
                         linewidth=0.0)
        if ylabel is not None:
            _ax.set_ylabel(ylabel, rotation=0, y=1.3, horizontalalignment='right')
        _ax.gridOn = False
        alt_labels_arr = self._calc_tick_labels(y, is_get_min=True)
        plt.setp(_ax, 'ylim', [alt_labels_arr[0], alt_labels_arr[-1]])
        plt.setp(_ax, 'yticks', alt_labels_arr[0:3])
        return _ax


def gradientBarPlot(x, y, colorZones):
    """
    :param x: for example time vector
    :param y: for example power or HR vector, the coloring will be done based on this value
    :param colorZones: vector to generate color levels, example Power Zones or HR zones, the same units as y
    :return:
    """

    # Create a 2-D ndarray to represent power color scheme
    colorMap = np.zeros([x.size, y.size])
    powerBar = (np.max(colorZones)/y.size) * np.arange(y.size)
    for kx in range(0, x.size-1, 1):
        # init the kx column of the colorMap with powerBar vector
        colorMap[kx, :] = powerBar
        instantYvalue = y[kx] # above this value the colorMap values will be set to zero
        setToZeroIndexes = np.where(powerBar > instantYvalue)
        colorMap[kx, setToZeroIndexes] = 0
    X, Y = np.meshgrid(x, powerBar)
    # Z = np.array([0.56, 0.76, 0.91, 1.06, 1.21, 1.51])/1.51
    Z = colorZones/np.max(colorZones)
    c = mcolors.ColorConverter().to_rgb
    # colors are generated based on Hue spectrum of Yellow
    white  = '#ffffff'
    lime   = '#00ff00'
    green  = '#80ff00'
    yellow = '#ffff00'
    orange = '#ffbf00'
    red    = '#ff4000'
    maroon = '#ff0000'

    rvb = make_colormap(
        [c(white), c(lime),    Z[0], # zone1 white:light_green
         c(lime), c(green),    Z[1], # zone2 light_green:lime
         c(green), c(yellow),  Z[2], # zone3 lime:yellow
         c(yellow), c(orange), Z[3], # zone4 yellow:orange
         c(orange), c(red),    Z[4], # zone5 orange:red
         c(red), c(maroon)        # zone6 red:maroon
         ])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.pcolormesh(X, Y, np.transpose(colorMap), cmap=rvb)
    plt.colorbar()
    # plt.plot(x, y, color = 'k', linewidth=1.5)
    plt.autoscale(tight=True)
    plt.show()


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


def gradientLinePlot(x, y, colorZones):
    """
    :param x: for example time vector
    :param y: for example power or HR vector, the coloring will be done based on this value
    :param colorZones: vector to generate color levels, example Power Zones or HR zones, the same units as y
    :return:
    """


if __name__ == "__main__":

    c = mcolors.ColorConverter().to_rgb
    # rvb = make_colormap(
    #     [c('red'), c('violet'), 0.33, c('violet'), c('blue'), 0.66, c('blue')])
    rvb = make_colormap(
        [c('white'), c('green'), 0.33, c('green'), c('yellow'), 0.66, c('yellow'), c('red')])
    N = 1000
    array_dg = np.random.uniform(0, 10, size=(N, 2))
    colors = np.random.uniform(-2, 2, size=(N,))
    plt.scatter(array_dg[:, 0], array_dg[:, 1], c=colors, cmap=rvb)
    plt.colorbar()
    plt.show()