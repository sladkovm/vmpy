import numpy as np
import pandas as pd
from vmpy.utils import list_to_ndarray


def test_to_ndarray_list():

    stream = [1,2,3]
    expected_y = np.asarray(stream)

    rv_y, rv_type = list_to_ndarray(stream)

    assert rv_type == list
    assert (rv_y == expected_y).all()


def test_to_ndarray_ndarray():

    stream = np.asarray([1,2,3])
    expected_y = np.asarray([1,2,3])

    rv_y, rv_type = list_to_ndarray(stream)

    assert rv_type == np.ndarray
    assert (rv_y == expected_y).all()


def test_to_ndarray_real_stream(test_stream):

    stream = test_stream['watts']

    rv_y, rv_type = list_to_ndarray(stream)

    assert rv_type == list
    assert type(rv_y) == np.ndarray
    assert rv_y.dtype != np.dtype('O')


def test_to_ndarray_real_stream_mix_type(test_stream_with_nans):

    stream = test_stream_with_nans['watts']

    rv_y, rv_type = list_to_ndarray(stream)

    assert rv_type == list
    assert type(rv_y) == np.ndarray
    assert rv_y.dtype != np.dtype('O')
