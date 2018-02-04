import pandas as pd
import logging
logger = logging.getLogger(__name__)

def to_ndarray(arg, **kwargs):
    """Convert an array-like input into a ndarray

    :param arg: array-like
    :param value: default=0, a value to use for None replacement
    :return y, type_arg: ndarray and type(arg)
    """
    type_arg = type(arg)

    if type_arg == list:

        y = pd.Series(arg).fillna(value=kwargs.get('value', 0))
        y = y.as_matrix()

    else:

        y = arg

    return y, type_arg