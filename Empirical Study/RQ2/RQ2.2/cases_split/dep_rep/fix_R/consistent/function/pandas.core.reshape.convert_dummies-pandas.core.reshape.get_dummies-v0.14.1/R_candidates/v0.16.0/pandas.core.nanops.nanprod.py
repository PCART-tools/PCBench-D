@disallow('M8','m8')
def nanprod(values, axis=None, skipna=True):
    mask = isnull(values)
    if skipna and not is_any_int_dtype(values):
        values = values.copy()
        values[mask] = 1
    result = values.prod(axis)
    return _maybe_null_out(result, axis, mask)
