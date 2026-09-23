def _get_fill_value(dtype, fill_value=None, fill_value_typ=None):
    """ return the correct fill value for the dtype of the values """
    if fill_value is not None:
        return fill_value
    if _na_ok_dtype(dtype):
        if fill_value_typ is None:
            return np.nan
        else:
            if fill_value_typ == '+inf':
                return np.inf
            else:
                return -np.inf
    else:
        if fill_value_typ is None:
            return tslib.iNaT
        else:
            if fill_value_typ == '+inf':
                # need the max int here
                return np.iinfo(np.int64).max
            else:
                return tslib.iNaT
