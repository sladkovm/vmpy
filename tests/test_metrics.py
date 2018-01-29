import numpy as np
from unittest import mock
from vmpy import metrics


def test_rolling_mean_list():

    stream = [1, 2, 3, 4, 5]

    expected = [1, 1.5, 2.5, 3.5, 4.5]

    assert metrics.rolling_mean(stream, 2) == expected


def test_rolling_mean_list_emwa():

    stream = list(np.ones(30))

    expected = list(np.ones(30))

    assert metrics.rolling_mean(stream, 2, type='emwa') == expected


def test_rolling_mean_list_with_moving():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]
    expected = [1, 1.5, 1.0, 2.0, 4.5]

    assert metrics.rolling_mean(stream, window=2, moving=moving) == expected


def test_rolling_mean_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])

    expected = np.asarray([1, 1.5, 2.5, 3.5, 4.5])

    assert (metrics.rolling_mean(stream, 2) == expected).all()


def test_rolling_mean_ndarray_with_moving():

    stream = np.asarray([1, 2, 3, 4, 5])
    moving = np.asarray([True, True, False, True, True], dtype=bool)

    expected = np.asarray([1, 1.5, 1.0, 2.0, 4.5])

    assert (metrics.rolling_mean(stream, window=2, moving=moving) == expected).all()


def test_rolling_mean_real_data(test_stream):

    rv = metrics.rolling_mean(test_stream['watts'],
                              moving=test_stream['moving'],
                              window=1)

    assert type(rv) == list
    assert rv == test_stream['watts']


def test_sanitize_stream_list():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]

    expected = [1, 2, 0.0, 4, 5]

    assert (metrics.sanitize_stream(stream, moving) == expected).all()


def test_sanitize_stream_list_with_replacement():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]

    expected = [1, 2, 10.0, 4, 5]

    assert (metrics.sanitize_stream(stream, moving, value=10.0) == expected).all()


def test_sanitize_stream_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])
    moving = np.asarray([True, True, False, True, True], dtype=bool)

    expected = np.asarray([1, 2, 0.0, 4, 5])

    assert (metrics.sanitize_stream(stream, moving) == expected).all()


@mock.patch('vmpy.metrics.rolling_mean')
def test_best_interval(test_rolling_mean):

    stream = [1,1,1,1,1]
    test_rolling_mean.return_value = stream

    assert metrics.best_interval(stream, 5) == 1


def test_normalized_power():

    stream = np.ones(30)
    moving = np.ones(30, dtype=bool)

    assert metrics.normalized_power(stream, moving) == 1


def test_normalized_power_xpower():

    stream = np.ones(30)
    moving = np.ones(30, dtype=bool)

    assert metrics.normalized_power(stream, moving, type='xPower') == 1
