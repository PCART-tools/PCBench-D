def _get_dtype(arr_or_dtype):
    if isinstance(arr_or_dtype, np.dtype):
        return arr_or_dtype
    elif isinstance(arr_or_dtype, type):
        return np.dtype(arr_or_dtype)
    elif isinstance(arr_or_dtype, CategoricalDtype):
        return CategoricalDtype()
    return arr_or_dtype.dtype
