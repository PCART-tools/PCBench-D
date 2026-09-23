def _get_data_algo(values, func_map):
    mask = None
    if com.is_float_dtype(values):
        f = func_map['float64']
        values = com._ensure_float64(values)

    elif com.needs_i8_conversion(values):

        # if we have NaT, punt to object dtype
        mask = com.isnull(values)
        if mask.ravel().any():
            f = func_map['generic']
            values = com._ensure_object(values)
            values[mask] = np.nan
        else:
            f = func_map['int64']
            values = values.view('i8')

    elif com.is_integer_dtype(values):
        f = func_map['int64']
        values = com._ensure_int64(values)
    else:
        f = func_map['generic']
        values = com._ensure_object(values)
    return f, values
