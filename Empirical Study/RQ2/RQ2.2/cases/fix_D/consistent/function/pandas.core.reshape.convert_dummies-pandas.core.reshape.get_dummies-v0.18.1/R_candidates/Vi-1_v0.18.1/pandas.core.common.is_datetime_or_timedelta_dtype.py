def is_datetime_or_timedelta_dtype(arr_or_dtype):
    tipo = _get_dtype_type(arr_or_dtype)
    return issubclass(tipo, (np.datetime64, np.timedelta64))
