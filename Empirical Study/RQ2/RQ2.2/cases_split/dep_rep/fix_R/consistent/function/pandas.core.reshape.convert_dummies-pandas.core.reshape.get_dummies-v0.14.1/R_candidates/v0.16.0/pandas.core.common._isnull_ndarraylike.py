def _isnull_ndarraylike(obj):

    values = getattr(obj, 'values', obj)
    dtype = values.dtype

    if dtype.kind in ('O', 'S', 'U'):
        if is_categorical_dtype(values):
            from pandas import Categorical
            if not isinstance(values, Categorical):
                values = values.values
            result = values.isnull()
        else:

            # Working around NumPy ticket 1542
            shape = values.shape

            if dtype.kind in ('S', 'U'):
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
    if isinstance(obj, ABCSeries):
        from pandas import Series
        result = Series(result, index=obj.index, name=obj.name, copy=False)

    return result
