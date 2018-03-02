import numpy as np
import pandas as pd
from unittest import mock
from vmpy import metrics


def test_wpk():

    power = [1,2,3]
    weight = 2

    rv = metrics.wpk(power, weight)
    expected = [0.5,1.0,1.5]
    assert type(rv) == list
    assert rv == expected

    rv = metrics.wpk(np.array(power), weight)
    expected = np.array([0.5, 1.0, 1.5])
    assert type(rv) == np.ndarray
    assert (rv == expected).all()

    rv = metrics.wpk(pd.Series(power), weight)
    expected = pd.Series([0.5, 1.0, 1.5])
    assert type(rv) == pd.Series
    assert (rv == expected).all()


@mock.patch('vmpy.metrics.rolling_mean')
def test_best_interval(test_rolling_mean):

    stream = [1,1,1,1,1]
    test_rolling_mean.return_value = stream

    assert metrics.best_interval(stream, 5) == 1


@mock.patch('vmpy.metrics.compute_zones')
def test_time_in_zones(tz):

    power = [0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
    tz.return_value = [1,2,3,4,5,6,7]

    rv = metrics.time_in_zones(power, ftp=1.0)
    expected = [1, 1, 1, 1, 1, 1, 1]

    assert type(rv) == list
    assert rv == expected


def test_zones_power_ftp_list():

    stream = [0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0]
    expected = [1, 2, 3, 4, 5, 6, 7]

    rv = metrics.compute_zones(stream, ftp=1.0)

    assert type(rv) == list
    assert rv == expected


def test_zones_heart_rate_lthr_list():

    stream = [0.6, 0.8, 0.9, 1.0, 1.1]
    expected = [1, 2, 3, 4, 5]

    rv = metrics.compute_zones(stream, lthr=1.0)

    assert type(rv) == list
    assert rv == expected


def test_zones_power_explicit_zones_list():

    stream = [1, 150, 210, 250, 300, 350, 450]
    expected = [1, 2, 3, 4, 5, 6, 7]

    rv = metrics.compute_zones(stream, zones=[-1, 144, 196, 235, 274, 313, 391, 10000])

    assert type(rv) == list
    assert rv == expected


def test_zones_heart_rate_explicit_zones_list():

    stream = [60, 120, 150, 160, 170, 180]
    expected = [1, 1, 2, 3, 4, 5]

    rv = metrics.compute_zones(stream, zones=[-1, 142, 155, 162, 174, 10000])

    assert type(rv) == list
    assert rv == expected


def test_zones_power_ftp_list_of_int():

    stream = [1, 2,]
    ftp=1.0
    expected = [4, 7,]

    rv = metrics.compute_zones(stream, ftp=ftp)

    assert type(rv) == list
    assert rv == expected


def test_zones_power_ftp_unordered_list():

    stream = [2, 1, 3]
    ftp=1.0
    expected = [7, 4, 7,]

    rv = metrics.compute_zones(stream, ftp=ftp)

    assert type(rv) == list
    assert rv == expected


def test_zones_power_ftp_ndarray():

    stream = np.asarray([0.55, 0.75, 0.9, 1.05, 1.2, 1.5, 10.0])
    expected = np.asarray(list(range(1,8)))

    rv = metrics.compute_zones(stream, ftp=1.0)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_normalized_power():

    stream = np.ones(30)
    moving = np.ones(30, dtype=bool)

    assert metrics.normalized_power(stream, moving) == 1

def test_normalized_power_xpower():

    stream = np.ones(30)
    moving = np.ones(30, dtype=bool)

    assert metrics.normalized_power(stream, moving, type='xPower') == 1


def test_relative_intensity():

    norm_power = 300.0
    threshold_power = 300.0

    assert metrics.relative_intensity(norm_power, threshold_power) == 1.0


def test_stress_score():

    norm_power = 300.0
    threshold_power = 300.0
    duration = 3600

    assert metrics.stress_score(norm_power, threshold_power, duration) == 100.0




def test_power_duration_curve():

    power = np.arange(101)
    rv = metrics.power_duration_curve(power)

    assert type(power) == np.ndarray
    assert rv[0] == 100.0
    assert rv[49] == 75.5
    assert rv[-1] == 50.5

def test_power_duration_curve_list():

    stream = [0, 0, 0]
    expected = [0, 0]

    rv = metrics.power_duration_curve(stream)

    assert type(rv) == list
    assert rv == expected


def test_power_duration_curve_ndarray():

    stream = np.zeros(3)
    expected = np.zeros(2)

    rv = metrics.power_duration_curve(stream)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_power_duration_curve_series():

    stream = pd.Series(np.zeros(3))
    expected = pd.Series(np.zeros(2))

    rv = metrics.power_duration_curve(stream)

    assert type(rv) == pd.Series
    assert (rv == expected).all()