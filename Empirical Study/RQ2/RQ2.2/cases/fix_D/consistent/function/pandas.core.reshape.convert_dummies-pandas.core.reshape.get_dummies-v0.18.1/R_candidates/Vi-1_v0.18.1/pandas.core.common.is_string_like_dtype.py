def is_string_like_dtype(arr_or_dtype):
    # exclude object as its a mixed dtype
    dtype = _get_dtype(arr_or_dtype)
    return dtype.kind in ('S', 'U')
