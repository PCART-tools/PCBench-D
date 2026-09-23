def is_bool_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return issubclass(tipo, np.bool_)
