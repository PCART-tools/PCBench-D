def is_datetimelike_v_numeric(a, b):
    # return if we have an i8 convertible and numeric comparison
    if not hasattr(a, 'dtype'):
        a = np.asarray(a)
    if not hasattr(b, 'dtype'):
        b = np.asarray(b)

    def is_numeric(x):
        return is_integer_dtype(x) or is_float_dtype(x)

    is_datetimelike = needs_i8_conversion
    return ((is_datetimelike(a) and is_numeric(b)) or
            (is_datetimelike(b) and is_numeric(a)))
