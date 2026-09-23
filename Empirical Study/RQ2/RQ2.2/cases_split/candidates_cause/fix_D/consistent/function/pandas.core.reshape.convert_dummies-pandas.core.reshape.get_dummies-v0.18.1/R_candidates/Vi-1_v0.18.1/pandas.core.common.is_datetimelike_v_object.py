def is_datetimelike_v_object(a, b):
    # return if we have an i8 convertible and object comparsion
    if not hasattr(a, 'dtype'):
        a = np.asarray(a)
    if not hasattr(b, 'dtype'):
        b = np.asarray(b)

    def f(x):
        return is_object_dtype(x)

    def is_object(x):
        return is_integer_dtype(x) or is_float_dtype(x)

    is_datetimelike = needs_i8_conversion
    return ((is_datetimelike(a) and is_object(b)) or
            (is_datetimelike(b) and is_object(a)))
