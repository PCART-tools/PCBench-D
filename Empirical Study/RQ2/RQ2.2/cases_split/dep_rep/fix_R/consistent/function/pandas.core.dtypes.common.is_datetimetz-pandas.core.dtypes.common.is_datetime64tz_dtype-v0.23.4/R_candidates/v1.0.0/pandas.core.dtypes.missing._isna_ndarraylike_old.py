def _isna_ndarraylike_old(obj):
    values = getattr(obj, "values", obj)
    dtype = values.dtype

    if is_string_dtype(dtype):
        # Working around NumPy ticket 1542
        shape = values.shape

        if is_string_like_dtype(dtype):
            result = np.zeros(values.shape, dtype=bool)
        else:
            result = np.empty(shape, dtype=bool)
            vec = libmissing.isnaobj_old(values.ravel())
            result[:] = vec.reshape(shape)

    elif is_datetime64_dtype(dtype):
        # this is the NaT pattern
        result = values.view("i8") == iNaT
    else:
        result = ~np.isfinite(values)

    # box
    if isinstance(obj, ABCSeries):
        result = obj._constructor(result, index=obj.index, name=obj.name, copy=False)

    return result
