def nanall(values, axis=None, skipna=True):
    values, mask, dtype, _ = _get_values(values, skipna, True, copy=skipna)
    return values.all(axis)
