def _get_data_algo(values, func_map):
    if is_float_dtype(values):
        f = func_map['float64']
        values = _ensure_float64(values)

    elif needs_i8_conversion(values):
        f = func_map['int64']
        values = values.view('i8')

    elif is_integer_dtype(values):
        f = func_map['int64']
        values = _ensure_int64(values)
    else:
        f = func_map['generic']
        values = _ensure_object(values)
    return f, values
