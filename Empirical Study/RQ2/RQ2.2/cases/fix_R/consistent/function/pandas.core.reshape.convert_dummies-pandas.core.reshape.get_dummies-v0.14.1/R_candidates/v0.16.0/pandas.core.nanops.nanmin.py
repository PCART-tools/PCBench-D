@bottleneck_switch()
def nanmin(values, axis=None, skipna=True):
    values, mask, dtype, dtype_max = _get_values(values, skipna,
                                                 fill_value_typ='+inf')

    # numpy 1.6.1 workaround in Python 3.x
    if is_object_dtype(values) and compat.PY3:
        if values.ndim > 1:
            apply_ax = axis if axis is not None else 0
            result = np.apply_along_axis(builtins.min, apply_ax, values)
        else:
            try:
                result = builtins.min(values)
            except:
                result = np.nan
    else:
        if ((axis is not None and values.shape[axis] == 0)
                or values.size == 0):
            try:
                result = ensure_float(values.sum(axis, dtype=dtype_max))
                result.fill(np.nan)
            except:
                result = np.nan
        else:
            result = values.min(axis)

    result = _wrap_results(result, dtype)
    return _maybe_null_out(result, axis, mask)
