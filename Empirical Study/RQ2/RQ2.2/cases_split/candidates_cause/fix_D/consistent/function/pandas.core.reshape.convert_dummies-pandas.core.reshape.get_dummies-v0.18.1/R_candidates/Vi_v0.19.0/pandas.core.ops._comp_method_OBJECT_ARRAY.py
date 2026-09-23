def _comp_method_OBJECT_ARRAY(op, x, y):
    if isinstance(y, list):
        y = lib.list_to_object_array(y)
    if isinstance(y, (np.ndarray, ABCSeries, ABCIndex)):
        if not is_object_dtype(y.dtype):
            y = y.astype(np.object_)

        if isinstance(y, (ABCSeries, ABCIndex)):
            y = y.values

        result = lib.vec_compare(x, y, op)
    else:
        result = lib.scalar_compare(x, y, op)
    return result
