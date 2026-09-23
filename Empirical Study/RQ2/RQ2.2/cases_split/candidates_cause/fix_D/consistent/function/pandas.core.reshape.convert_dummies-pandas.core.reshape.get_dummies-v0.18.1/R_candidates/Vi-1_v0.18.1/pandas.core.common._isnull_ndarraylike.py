def _isnull_ndarraylike(obj):

    values = getattr(obj, 'values', obj)
    dtype = values.dtype

    if is_string_dtype(dtype):
        if is_categorical_dtype(values):
            from pandas import Categorical
            if not isinstance(values, Categorical):
                values = values.values
            result = values.isnull()
        else:

            # Working around NumPy ticket 1542
            shape = values.shape

            if is_string_like_dtype(dtype):
                result = np.zeros(values.shape, dtype=bool)
            else:
                result = np.empty(shape, dtype=bool)
                vec = lib.isnullobj(values.ravel())
                result[...] = vec.reshape(shape)

    elif is_datetimelike(obj):
        # this is the NaT pattern
        result = values.view('i8') == tslib.iNaT
    else:
        result = np.isnan(values)

    # box
    if isinstance(obj, gt.ABCSeries):
        from pandas import Series
        result = Series(result, index=obj.index, name=obj.name, copy=False)

    return result
