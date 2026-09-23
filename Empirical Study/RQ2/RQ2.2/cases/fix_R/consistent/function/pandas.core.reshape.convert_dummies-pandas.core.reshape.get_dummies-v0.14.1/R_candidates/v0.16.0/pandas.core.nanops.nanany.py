def nanany(values, axis=None, skipna=True):
    values, mask, dtype, _ = _get_values(values, skipna, False, copy=skipna)
    return values.any(axis)
