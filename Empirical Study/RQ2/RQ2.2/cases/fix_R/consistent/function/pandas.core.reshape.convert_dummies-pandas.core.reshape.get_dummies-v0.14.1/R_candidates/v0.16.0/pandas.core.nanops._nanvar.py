def _nanvar(values, axis=None, skipna=True, ddof=1):
    # private nanvar calculator
    mask = isnull(values)
    if is_any_int_dtype(values):
        values = values.astype('f8')

    count, d = _get_counts_nanvar(mask, axis, ddof)

    if skipna:
        values = values.copy()
        np.putmask(values, mask, 0)

    X = _ensure_numeric(values.sum(axis))
    XX = _ensure_numeric((values ** 2).sum(axis))
    return np.fabs((XX - X ** 2 / count) / d)
