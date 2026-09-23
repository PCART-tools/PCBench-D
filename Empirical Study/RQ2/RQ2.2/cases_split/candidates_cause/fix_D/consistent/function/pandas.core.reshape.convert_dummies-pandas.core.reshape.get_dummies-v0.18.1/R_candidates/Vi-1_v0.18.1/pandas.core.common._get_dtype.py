def _get_dtype(arr_or_dtype):
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype
    elif isinstance(arr_or_dtype, type):
        return np.dtype(arr_or_dtype)
    elif isinstance(arr_or_dtype, gt.CategoricalDtype):
        return arr_or_dtype
    elif isinstance(arr_or_dtype, gt.DatetimeTZDtype):
        return arr_or_dtype
    elif isinstance(arr_or_dtype, compat.string_types):
        if is_categorical_dtype(arr_or_dtype):
            return gt.CategoricalDtype.construct_from_string(arr_or_dtype)
        elif is_datetime64tz_dtype(arr_or_dtype):
            return gt.DatetimeTZDtype.construct_from_string(arr_or_dtype)

    if hasattr(arr_or_dtype, 'dtype'):
        arr_or_dtype = arr_or_dtype.dtype
    return np.dtype(arr_or_dtype)
