def coerce_to_dtypes(result, dtypes):
    """
    given a dtypes and a result set, coerce the result elements to the
    dtypes
    """
    if len(result) != len(dtypes):
        raise AssertionError("_coerce_to_dtypes requires equal len arrays")

    def conv(r, dtype):
        if np.any(isna(r)):
            pass
        elif dtype == DT64NS_DTYPE:
            r = tslibs.Timestamp(r)
        elif dtype == TD64NS_DTYPE:
            r = tslibs.Timedelta(r)
        elif dtype == np.bool_:
            # messy. non 0/1 integers do not get converted.
            if is_integer(r) and r not in [0, 1]:
                return int(r)
            r = bool(r)
        elif dtype.kind == "f":
            r = float(r)
        elif dtype.kind == "i":
            r = int(r)

        return r

    return [conv(r, dtype) for r, dtype in zip(result, dtypes)]
