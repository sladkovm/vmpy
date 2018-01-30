import numpy as np
from vmpy import preprocess


def test_sanitize_stream_list():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]

    expected = [1, 2, 0.0, 4, 5]

    assert (preprocess.sanitize_stream(stream, moving) == expected).all()


def test_sanitize_stream_list_with_replacement():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]

    expected = [1, 2, 10.0, 4, 5]

    assert (preprocess.sanitize_stream(stream, moving, value=10.0) == expected).all()

def test_sanitize_stream_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])
    moving = np.asarray([True, True, False, True, True], dtype=bool)

    expected = np.asarray([1, 2, 0.0, 4, 5])

    assert (preprocess.sanitize_stream(stream, moving) == expected).all()



def test_rolling_mean_list():

    stream = [1, 2, 3, 4, 5]

    expected = [1, 1.5, 2.5, 3.5, 4.5]

    assert preprocess.rolling_mean(stream, 2) == expected


def test_rolling_mean_list_emwa():

    stream = list(np.ones(30))

    expected = list(np.ones(30))

    assert preprocess.rolling_mean(stream, 2, type='emwa') == expected


def test_rolling_mean_list_with_moving():

    stream = [1, 2, 3, 4, 5]
    moving = [True, True, False, True, True]
    expected = [1, 1.5, 1.0, 2.0, 4.5]

    assert preprocess.rolling_mean(stream, window=2, moving=moving) == expected


def test_rolling_mean_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])

    expected = np.asarray([1, 1.5, 2.5, 3.5, 4.5])

    assert (preprocess.rolling_mean(stream, 2) == expected).all()


def test_rolling_mean_ndarray_with_moving():

    stream = np.asarray([1, 2, 3, 4, 5])
    moving = np.asarray([True, True, False, True, True], dtype=bool)

    expected = np.asarray([1, 1.5, 1.0, 2.0, 4.5])

    assert (preprocess.rolling_mean(stream, window=2, moving=moving) == expected).all()


def test_rolling_mean_real_data(test_stream):

    rv = preprocess.rolling_mean(test_stream['watts'],
                              moving=test_stream['moving'],
                              window=1)

    assert type(rv) == list
    assert rv == test_stream['watts']