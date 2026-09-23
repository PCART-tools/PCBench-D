def mode(values):
    """Returns the mode or mode(s) of the passed Series or ndarray (sorted)"""
    # must sort because hash order isn't necessarily defined.
    from pandas.core.series import Series

    if isinstance(values, Series):
        constructor = values._constructor
        values = values.values
    else:
        values = np.asanyarray(values)
        constructor = Series

    dtype = values.dtype
    if com.is_integer_dtype(values):
        values = com._ensure_int64(values)
        result = constructor(sorted(htable.mode_int64(values)), dtype=dtype)

    elif issubclass(values.dtype.type, (np.datetime64, np.timedelta64)):
        dtype = values.dtype
        values = values.view(np.int64)
        result = constructor(sorted(htable.mode_int64(values)), dtype=dtype)

    elif com.is_categorical_dtype(values):
        result = constructor(values.mode())
    else:
        mask = com.isnull(values)
        values = com._ensure_object(values)
        res = htable.mode_object(values, mask)
        try:
            res = sorted(res)
        except TypeError as e:
            warn("Unable to sort modes: %s" % e)
        result = constructor(res, dtype=dtype)

    return result
