import pandas as pd
import logging
logger = logging.getLogger(__name__)

def to_ndarray(arg, **kwargs):
    """Convert an array-like input into a ndarray

    Parameters
    ----------
    arg : array-like
    value : number, optional
        A value to use for None replacement, default=0

    Returns
    -------
    y : ndarray
    type_arg : type(arg)
    """
    type_arg = type(arg)

    if type_arg == list:

        y = pd.Series(arg).fillna(value=kwargs.get('value', 0))
        y = y.as_matrix()

    else:

        y = arg

    return y, type_arg