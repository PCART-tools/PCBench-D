def is_datetime64_dtype(arr_or_dtype):
    try:
        tipo = _get_dtype_type(arr_or_dtype)
    except TypeError:
        return False
    return issubclass(tipo, np.datetime64)
