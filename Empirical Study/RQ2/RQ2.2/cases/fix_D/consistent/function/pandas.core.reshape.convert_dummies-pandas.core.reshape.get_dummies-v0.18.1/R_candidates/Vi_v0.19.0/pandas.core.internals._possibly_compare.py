def _possibly_compare(a, b, op):

    is_a_array = isinstance(a, np.ndarray)
    is_b_array = isinstance(b, np.ndarray)

    # numpy deprecation warning to have i8 vs integer comparisions
    if is_datetimelike_v_numeric(a, b):
        result = False

    # numpy deprecation warning if comparing numeric vs string-like
    elif is_numeric_v_string_like(a, b):
        result = False

    else:
        result = op(a, b)

    if is_scalar(result) and (is_a_array or is_b_array):
        type_names = [type(a).__name__, type(b).__name__]

        if is_a_array:
            type_names[0] = 'ndarray(dtype=%s)' % a.dtype

        if is_b_array:
            type_names[1] = 'ndarray(dtype=%s)' % b.dtype

        raise TypeError("Cannot compare types %r and %r" % tuple(type_names))
    return result
