import numpy as np
from vmpy.utils import to_ndarray


def test_to_ndarray_list():

    stream = [1,2,3]
    expected_y = np.asarray(stream)

    rv_y, rv_type = to_ndarray(stream)

    assert rv_type == list
    assert (rv_y == expected_y).all()


def test_to_ndarray_ndarray():

    stream = np.asarray([1,2,3])
    expected_y = np.asarray([1,2,3])

    rv_y, rv_type = to_ndarray(stream)

    assert rv_type == np.ndarray
    assert (rv_y == expected_y).all()