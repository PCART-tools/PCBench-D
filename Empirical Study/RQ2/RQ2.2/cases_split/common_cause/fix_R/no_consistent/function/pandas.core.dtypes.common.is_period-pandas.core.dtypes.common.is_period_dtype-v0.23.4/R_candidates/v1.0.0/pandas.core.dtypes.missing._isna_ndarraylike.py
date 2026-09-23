def _isna_ndarraylike(obj):
    is_extension = is_extension_array_dtype(obj)

    if not is_extension:
        # Avoid accessing `.values` on things like
        # PeriodIndex, which may be expensive.
        values = getattr(obj, "values", obj)
    else:
        values = obj

    dtype = values.dtype

    if is_extension:
        if isinstance(obj, (ABCIndexClass, ABCSeries)):
            values = obj._values
        else:
            values = obj
        result = values.isna()
    elif isinstance(obj, ABCDatetimeArray):
        return obj.isna()
    elif is_string_dtype(dtype):
        # Working around NumPy ticket 1542
        shape = values.shape

        if is_string_like_dtype(dtype):
            # object array of strings
            result = np.zeros(values.shape, dtype=bool)
        else:
            # object array of non-strings
            result = np.empty(shape, dtype=bool)
            vec = libmissing.isnaobj(values.ravel())
            result[...] = vec.reshape(shape)

    elif needs_i8_conversion(dtype):
        # this is the NaT pattern
        result = values.view("i8") == iNaT
    else:
        result = np.isnan(values)

    # box
    if isinstance(obj, ABCSeries):
        result = obj._constructor(result, index=obj.index, name=obj.name, copy=False)

    return result
