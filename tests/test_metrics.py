# import numpy as np
# from unittest import mock
# from vmpy import metrics
#
#
# @mock.patch('vmpy.metrics.rolling_mean')
# def test_best_interval(test_rolling_mean):
#
#     stream = [1,1,1,1,1]
#     test_rolling_mean.return_value = stream
#
#     assert metrics.best_interval(stream, 5) == 1
#
#
# def test_normalized_power():
#
#     stream = np.ones(30)
#     moving = np.ones(30, dtype=bool)
#
#     assert metrics.normalized_power(stream, moving) == 1
#
#
# def test_normalized_power_xpower():
#
#     stream = np.ones(30)
#     moving = np.ones(30, dtype=bool)
#
#     assert metrics.normalized_power(stream, moving, type='xPower') == 1
#
#
# def test_relative_intensity():
#
#     norm_power = 300.0
#     threshold_power = 300.0
#
#     assert metrics.relative_intensity(norm_power, threshold_power) == 1.0
#
#
# def test_stress_score():
#
#     norm_power = 300.0
#     threshold_power = 300.0
#     duration = 3600
#
#     assert metrics.stress_score(norm_power, threshold_power, duration) == 100.0