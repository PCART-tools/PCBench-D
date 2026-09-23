def _coerce_to_dtype(dtype):
    """ coerce a string / np.dtype to a dtype """
    if is_categorical_dtype(dtype):
        dtype = gt.CategoricalDtype()
    elif is_datetime64tz_dtype(dtype):
        dtype = gt.DatetimeTZDtype(dtype)
    else:
        dtype = np.dtype(dtype)
    return dtype
