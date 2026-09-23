def needs_i8_conversion(arr_or_dtype):
    return (is_datetime_or_timedelta_dtype(arr_or_dtype) or
            is_datetime64tz_dtype(arr_or_dtype))
