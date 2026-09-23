def is_string_dtype(arr_or_dtype):
    dtype = _get_dtype(arr_or_dtype)
    return dtype.kind in ('O', 'S', 'U')
