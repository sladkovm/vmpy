import numpy as np


def to_ndarray(arg):
    """Returns type of the input and converts to ndarray

    :param arg: array-like
    :return y, type_arg: ndarray and type(arg)
    """
    type_arg = type(arg)
    if type_arg == list:
        y = np.asarray(arg)
    else:
        y = arg

    return y, type_arg