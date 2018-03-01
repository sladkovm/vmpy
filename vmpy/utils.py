import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)


def list_to_ndarray(arg, **kwargs):
    """Convert an array-like input into a ndarray

    NaN value replacement is controlled by keyword arguments

    Parameters
    ----------
    arg : array-like
    value : number, optional
        A value to use for None replacement, default=np.nan

    Returns
    -------
    y : ndarray
    arg_type : type(arg)
    """
    arg_type = type(arg)

    if arg_type == list:

        y = pd.Series(arg).fillna(value=kwargs.get('value', np.nan))
        y = y.as_matrix()

    else:

        y = arg

    return y, arg_type
