def is_floating_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return isinstance(tipo, np.floating)
