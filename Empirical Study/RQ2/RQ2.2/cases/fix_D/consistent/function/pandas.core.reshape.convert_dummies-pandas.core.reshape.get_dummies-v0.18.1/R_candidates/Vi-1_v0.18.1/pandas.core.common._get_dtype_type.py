def _get_dtype_type(arr_or_dtype):
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype.type
    elif isinstance(arr_or_dtype, type):
        return np.dtype(arr_or_dtype).type
    elif isinstance(arr_or_dtype, gt.CategoricalDtype):
        return gt.CategoricalDtypeType
    elif isinstance(arr_or_dtype, gt.DatetimeTZDtype):
        return gt.DatetimeTZDtypeType
    elif isinstance(arr_or_dtype, compat.string_types):
        if is_categorical_dtype(arr_or_dtype):
            return gt.CategoricalDtypeType
        elif is_datetime64tz_dtype(arr_or_dtype):
            return gt.DatetimeTZDtypeType
        return _get_dtype_type(np.dtype(arr_or_dtype))
    try:
        return arr_or_dtype.dtype.type
    except AttributeError:
        return type(None)
