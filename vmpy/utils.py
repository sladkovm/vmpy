import numpy as np
import pandas as pd
import logging
logger = logging.getLogger(__name__)

def to_ndarray(arg, **kwargs):
    """Returns type of the input and converts to ndarray

    :param arg: array-like
    :return y, type_arg: ndarray and type(arg)
    """
    type_arg = type(arg)

    if type_arg == list:

        if None not in arg:

            y = np.asarray_chkfinite(arg)

        else:

            logger.warning(r"""NaN or Inf was detected in the list!
                            Retrying with pandas and fillna with {}
                            """.format(kwargs.get('value', 0)))

            y = pd.Series(arg).fillna(value=kwargs.get('value', 0))
            y = y.as_matrix()

    else:

        y = arg

    return y, type_arg