import numpy as np
import pandas as pd
from vmpy import streams


def test_mask_filter_mask_none():

    stream = [1, 2, 3]
    mask = None

    expected = [1, 2, 3]

    rv = streams.mask_fill(stream, mask)

    assert type(rv) == list
    assert rv == expected


def test_mask_filter_list():

    stream = [1, 2, 3, 4, 5]
    mask = [True, True, False, True, True]

    expected = [1, 2, 0.0, 4, 5]

    rv = streams.mask_fill(stream, mask)

    assert type(rv) == list
    assert rv == expected


def test_mask_filter_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])
    mask = np.asarray([True, True, False, True, True], dtype=bool)

    expected = np.asarray([1, 2, 0.0, 4, 5])
    rv = streams.mask_fill(stream, mask)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_mask_filter_series():

    stream = pd.Series([1, 2, 3, 4, 5])
    mask = pd.Series([True, True, False, True, True])

    expected = pd.Series([1, 2, 0.0, 4, 5])
    rv = streams.mask_fill(stream, mask)

    assert type(rv) == pd.Series
    assert (rv == expected).all()


def test_mask_filter_list_with_replacement():

    stream = [1, 2, 3, 4, 5]
    mask = [True, True, False, True, True]

    expected = [1, 2, 10.0, 4, 5]

    rv = streams.mask_fill(stream, mask, value=10.0)

    assert type(rv) == list
    assert rv == expected


def test_rolling_mean_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])
    expected = np.asarray([1, 1.5, 2.5, 3.5, 4.5])

    rv = streams.rolling_mean(stream, 2)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()


def test_rolling_mean_list():

    stream = [1, 2, 3, 4, 5]
    expected = [1, 1.5, 2.5, 3.5, 4.5]
    rv = streams.rolling_mean(stream, 2)

    assert type(rv) == list
    assert rv == expected


def test_rolling_mean_list_with_mask():

    stream = [1, 2, 3, 4, 5]
    mask = [True, True, False, True, True]
    expected = [1, 1.5, 1.0, 2.0, 4.5]
    rv = streams.rolling_mean(stream, window=2, mask=mask)

    assert type(rv) == list
    assert  rv == expected


def test_rolling_mean_with_mask_ndarray():

    stream = np.asarray([1, 2, 3, 4, 5])
    mask = np.asarray([True, True, False, True, True], dtype=bool)
    expected = np.asarray([1, 1.5, 1.0, 2.0, 4.5])
    rv = streams.rolling_mean(stream, window=2, mask=mask)

    assert type(rv) == np.ndarray
    assert  (rv == expected).all()


def test_rolling_mean_list_emwa():

    stream = list(np.ones(30))
    expected = list(np.ones(30))
    rv = streams.rolling_mean(stream, 2, type='ewma')

    assert type(rv) == list
    assert rv == expected


def test_rolling_mean_real_data(test_stream):

    rv = streams.rolling_mean(test_stream['watts'],
                                 mask=test_stream['moving'],
                                 window=1)

    assert type(rv) == list
    assert rv == test_stream['watts']


def test_hampel_filter():

    stream = np.ones(60)
    stream[-1] = 2

    rv = streams.median_filter(stream)
    assert type(rv) == np.ndarray
    assert (rv == np.ones(60)).all()


def test_hampel_filter_list():

    stream = np.ones(60)
    stream[-1] = 2
    stream = stream.tolist()

    expected = np.ones(60)
    expected = expected.tolist()

    rv = streams.median_filter(stream)

    assert type(rv) == list
    assert rv == expected


def test_hampel_filter_with_replacement():

    stream = np.ones(60)
    stream[-1] = 2

    expected = np.ones(60)
    expected[-1] = 10

    rv = streams.median_filter(stream, value=10)

    assert type(rv) == np.ndarray
    assert (rv == expected).all()