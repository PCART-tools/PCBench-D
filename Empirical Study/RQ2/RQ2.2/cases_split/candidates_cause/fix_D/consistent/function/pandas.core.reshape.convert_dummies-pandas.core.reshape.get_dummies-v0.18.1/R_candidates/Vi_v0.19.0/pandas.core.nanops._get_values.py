def _get_values(values, skipna, fill_value=None, fill_value_typ=None,
                isfinite=False, copy=True):
    """ utility to get the values view, mask, dtype
    if necessary copy and mask using the specified fill_value
    copy = True will force the copy
    """
    values = _values_from_object(values)
    if isfinite:
        mask = _isfinite(values)
    else:
        mask = isnull(values)

    dtype = values.dtype
    dtype_ok = _na_ok_dtype(dtype)

    # get our fill value (in case we need to provide an alternative
    # dtype for it)
    fill_value = _get_fill_value(dtype, fill_value=fill_value,
                                 fill_value_typ=fill_value_typ)

    if skipna:
        if copy:
            values = values.copy()
        if dtype_ok:
            np.putmask(values, mask, fill_value)

        # promote if needed
        else:
            values, changed = _maybe_upcast_putmask(values, mask, fill_value)

    elif copy:
        values = values.copy()

    values = _view_if_needed(values)

    # return a platform independent precision dtype
    dtype_max = dtype
    if is_integer_dtype(dtype) or is_bool_dtype(dtype):
        dtype_max = np.int64
    elif is_float_dtype(dtype):
        dtype_max = np.float64

    return values, mask, dtype, dtype_max
