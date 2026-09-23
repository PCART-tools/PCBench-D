def is_numeric_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return (issubclass(tipo, (np.number, np.bool_)) and
            not issubclass(tipo, (np.datetime64, np.timedelta64)))
