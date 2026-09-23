def is_datetime64_any_dtype(arr_or_dtype):
    return (is_datetime64_dtype(arr_or_dtype) or
            is_datetime64tz_dtype(arr_or_dtype))
