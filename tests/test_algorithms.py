import numpy as np
from vmpy.algorithms import power_duration_curve


def test_power_duration_curve_list():

    assert power_duration_curve([0, 0, 0]) == [0, 0]


def test_power_duration_curve_ndarray():

    assert (power_duration_curve(np.zeros(3)) == np.zeros(2)).all()