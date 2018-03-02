import numpy as np
import pandas as pd
from vmpy.algorithms import power_duration_curve


def test_power_duration_curve():

    power = np.arange(101)
    rv = power_duration_curve(power)

    assert type(power) == np.ndarray
    assert rv[0] == 100.0
    assert rv[49] == 75.5
    assert rv[-1] == 50.5

def test_power_duration_curve_list():

    stream = [0, 0, 0]
    expected = [0, 0]

    rv = power_duration_curve(stream)

    assert type(rv) == list
    assert rv == expected


def test_power_duration_curve_ndarray():

    stream = np.zeros(3)
    expected = np.zeros(2)

    rv = power_duration_curve(stream)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_power_duration_curve_series():

    stream = pd.Series(np.zeros(3))
    expected = pd.Series(np.zeros(2))

    rv = power_duration_curve(stream)

    assert type(rv) == pd.Series
    assert (rv == expected).all()