from vmpy.algorithms import power_duration_curve


def test_power_duration_curve():

    assert power_duration_curve([0, 0, 0]) == [0, 0]