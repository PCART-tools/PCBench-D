def _isfinite(values):
    if is_datetime_or_timedelta_dtype(values):
        return isnull(values)
    if (is_complex_dtype(values) or is_float_dtype(values) or
            is_integer_dtype(values) or is_bool_dtype(values)):
        return ~np.isfinite(values)
    return ~np.isfinite(values.astype('float64'))
