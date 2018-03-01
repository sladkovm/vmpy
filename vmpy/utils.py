import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)


# def list_to_ndarray(arg, **kwargs):
#     """Convert an array-like input into a ndarray
#
#     NaN value replacement is controlled by keyword arguments
#
#     Parameters
#     ----------
#     arg : array-like
#     value : number, optional
#         A value to use for None replacement, default=np.nan
#
#     Returns
#     -------
#     y : ndarray
#     arg_type : type(arg)
#     """
#     arg_type = type(arg)
#
#     if arg_type == list:
#
#         y = pd.Series(arg).fillna(value=kwargs.get('value', np.nan))
#         y = y.as_matrix()
#
#     else:
#
#         y = arg
#
#     return y, arg_type


def cast_array_to_original_type(arg, arg_type):
    """

    Parameters
    ----------
    arg: array-like
    arg_type: type

    Returns
    -------
    casted : array-like of the type of arg_type
    """

    if arg_type == list:
        return list(arg)


    elif arg_type == np.ndarray:
        return np.array(arg)

    elif arg_type == pd.Series:
        return pd.Series(arg)

    else:
        raise ValueError("arg_type must be list, ndarray or pd.Series")
