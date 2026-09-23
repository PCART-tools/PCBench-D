def is_datetime64_ns_dtype(arr_or_dtype):
    try:
        tipo = _get_dtype(arr_or_dtype)
    except TypeError:
        return False
    return tipo == _NS_DTYPE
