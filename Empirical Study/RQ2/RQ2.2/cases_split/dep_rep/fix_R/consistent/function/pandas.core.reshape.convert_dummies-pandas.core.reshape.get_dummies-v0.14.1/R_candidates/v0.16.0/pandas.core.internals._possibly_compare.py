def _possibly_compare(a, b, op):
    res = op(a, b)
    is_a_array = isinstance(a, np.ndarray)
    is_b_array = isinstance(b, np.ndarray)
    if np.isscalar(res) and (is_a_array or is_b_array):
        type_names = [type(a).__name__, type(b).__name__]

        if is_a_array:
            type_names[0] = 'ndarray(dtype=%s)' % a.dtype

        if is_b_array:
            type_names[1] = 'ndarray(dtype=%s)' % b.dtype

        raise TypeError("Cannot compare types %r and %r" % tuple(type_names))
    return res
