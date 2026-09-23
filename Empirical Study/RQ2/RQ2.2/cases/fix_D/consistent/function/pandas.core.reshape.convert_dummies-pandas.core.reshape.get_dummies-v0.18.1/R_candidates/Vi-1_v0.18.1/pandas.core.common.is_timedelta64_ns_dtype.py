def is_timedelta64_ns_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return tipo == _TD_DTYPE
