def is_any_int_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return issubclass(tipo, np.integer)
