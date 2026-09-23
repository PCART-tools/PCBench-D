def is_datetime64_ns_dtype(arr_or_dtype):
    tipo = _get_dtype(arr_or_dtype)
    return tipo == _NS_DTYPE
