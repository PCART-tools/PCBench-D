def is_int_or_datetime_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return (issubclass(tipo, np.integer) or
            issubclass(tipo, (np.datetime64, np.timedelta64)))
