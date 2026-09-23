def _get_dtype_type(arr_or_dtype):
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype.type
    elif isinstance(arr_or_dtype, type):
        return np.dtype(arr_or_dtype).type
    elif isinstance(arr_or_dtype, CategoricalDtype):
        return CategoricalDtypeType
    return arr_or_dtype.dtype.type
