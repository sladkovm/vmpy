import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm

class SimpleStravaPlot(object):

    @staticmethod
    def plot_strava_analysis_simple(activity, **kwargs):
        """Line2D plots of velocity_smooth, power, heartrate"""
        _style = kwargs.get('style', 'ggplot')
        plt.style.use(_style)
        _title = kwargs.get('title', 'Strava analysis plot')

        _distance = activity.distance
        _speed = activity.speed
        _power = activity.power_ewma25
        _heartrate = activity.heartrate
        _altitude = activity.altitude

        f, axarr = plt.subplots(3, sharex=True)

        ax_speed = axarr[0]
        ax_speed_bg = SimpleStravaPlot._add_elevation_background(ax_speed, _distance, _altitude,
                                                                 ylabel='Altitude [m]')
        ax_speed = SimpleStravaPlot._add_line_plot(ax_speed, _distance, _speed,
                                                   ylabel='Speed [km/h]', title=_title)

        ax_power = axarr[1]
        ax_speed_bg = SimpleStravaPlot._add_elevation_background(ax_power, _distance, _altitude,
                                                                 ylabel='Altitude [m]')
        ax_power = SimpleStravaPlot._add_line_plot(ax_power, _distance, _power,
                                                   ylabel='Power [Watts]')

        ax_heartrate = axarr[2]
        ax_speed_bg = SimpleStravaPlot._add_elevation_background(ax_heartrate, _distance, _altitude,
                                                                 ylabel='Altitude [m]')
        ax_heartrate = SimpleStravaPlot._add_line_plot(ax_heartrate, _distance, _heartrate,
                                                       xlabel='Distance [km]', ylabel='Heartrate [bpm]')
        plt.show()

    @staticmethod
    def _add_line_plot(axes, x, y, **kwargs):
        xlabel = kwargs.get('xlabel', None)
        ylabel = kwargs.get('ylabel', None)
        title = kwargs.get('title', None)
        axes.plot(x, y)
        if xlabel is not None:
            axes.set_xlabel(xlabel)
        if ylabel is not None:
            axes.set_ylabel(ylabel)
        if title is not None:
            axes.set_title(title)
        return axes

    @staticmethod
    def _add_elevation_background(axes, x, y, **kwargs):
        """ Elevation profile background """
        ylabel = kwargs.get('ylabel', None)
        _ax = axes.twinx()
        _ax.fill_between(x, np.ones(y.shape)*np.min(y), y, facecolor='grey', alpha=0.5, linewidth=0.0)
        if ylabel is not None:
            _ax.set_ylabel(ylabel)
        _ax.gridOn = False
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