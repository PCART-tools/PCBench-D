def _infer_fill_value(val):
    """
    infer the fill value for the nan/NaT from the provided
    scalar/ndarray/list-like if we are a NaT, return the correct dtyped
    element to provide proper block construction
    """

    if not is_list_like(val):
        val = [val]
    val = np.array(val, copy=False)
    if is_datetimelike(val):
        return np.array('NaT', dtype=val.dtype)
    elif is_object_dtype(val.dtype):
        dtype = lib.infer_dtype(_ensure_object(val))
        if dtype in ['datetime', 'datetime64']:
            return np.array('NaT', dtype=_NS_DTYPE)
        elif dtype in ['timedelta', 'timedelta64']:
            return np.array('NaT', dtype=_TD_DTYPE)
    return np.nan
