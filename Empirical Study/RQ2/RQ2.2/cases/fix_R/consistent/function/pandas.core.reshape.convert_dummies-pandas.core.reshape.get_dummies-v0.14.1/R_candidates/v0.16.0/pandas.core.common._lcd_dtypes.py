def _lcd_dtypes(a_dtype, b_dtype):
    """ return the lcd dtype to hold these types """

    if is_datetime64_dtype(a_dtype) or is_datetime64_dtype(b_dtype):
        return _NS_DTYPE
    elif is_timedelta64_dtype(a_dtype) or is_timedelta64_dtype(b_dtype):
        return _TD_DTYPE
    elif is_complex_dtype(a_dtype):
        if is_complex_dtype(b_dtype):
            return a_dtype
        return np.float64
    elif is_integer_dtype(a_dtype):
        if is_integer_dtype(b_dtype):
            if a_dtype.itemsize == b_dtype.itemsize:
                return a_dtype
            return np.int64
        return np.float64
    elif is_float_dtype(a_dtype):
        if is_float_dtype(b_dtype):
            if a_dtype.itemsize == b_dtype.itemsize:
                return a_dtype
            else:
                return np.float64
        elif is_integer(b_dtype):
            return np.float64
    return np.object
