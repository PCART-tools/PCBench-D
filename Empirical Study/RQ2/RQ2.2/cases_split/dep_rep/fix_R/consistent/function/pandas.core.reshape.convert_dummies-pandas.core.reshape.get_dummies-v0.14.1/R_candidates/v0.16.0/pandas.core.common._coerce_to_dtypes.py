def _coerce_to_dtypes(result, dtypes):
    """ given a dtypes and a result set, coerce the result elements to the
    dtypes
    """
    if len(result) != len(dtypes):
        raise AssertionError("_coerce_to_dtypes requires equal len arrays")

    from pandas.tseries.timedeltas import _coerce_scalar_to_timedelta_type

    def conv(r, dtype):
        try:
            if isnull(r):
                pass
            elif dtype == _NS_DTYPE:
                r = lib.Timestamp(r)
            elif dtype == _TD_DTYPE:
                r = _coerce_scalar_to_timedelta_type(r)
            elif dtype == np.bool_:
                # messy. non 0/1 integers do not get converted.
                if is_integer(r) and r not in [0,1]:
                    return int(r)
                r = bool(r)
            elif dtype.kind == 'f':
                r = float(r)
            elif dtype.kind == 'i':
                r = int(r)
        except:
            pass

        return r

    return [conv(r, dtype) for r, dtype in zip(result, dtypes)]
