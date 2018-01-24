import numpy as np
from vmpy import metrics


def test_rolling_mean_list():

    stream = [1, 2, 3, 4, 5]

    expected = [1, 1.5, 2.5, 3.5, 4.5]

    assert metrics.rolling_mean(stream, 2) == expected


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