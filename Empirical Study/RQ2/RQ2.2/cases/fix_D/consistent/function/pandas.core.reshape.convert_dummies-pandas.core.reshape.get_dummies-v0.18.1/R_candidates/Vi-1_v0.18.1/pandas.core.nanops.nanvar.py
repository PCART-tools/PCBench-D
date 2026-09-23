@disallow('M8')
@bottleneck_switch(ddof=1)
def nanvar(values, axis=None, skipna=True, ddof=1):

    dtype = values.dtype
    mask = isnull(values)
    if is_any_int_dtype(values):
        values = values.astype('f8')
        values[mask] = np.nan

    if is_float_dtype(values):
        count, d = _get_counts_nanvar(mask, axis, ddof, values.dtype)
    else:
        count, d = _get_counts_nanvar(mask, axis, ddof)

    if skipna:
        values = values.copy()
        np.putmask(values, mask, 0)

    # xref GH10242
    # Compute variance via two-pass algorithm, which is stable against
    # cancellation errors and relatively accurate for small numbers of
    # observations.
    #
    # See https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    avg = _ensure_numeric(values.sum(axis=axis, dtype=np.float64)) / count
    if axis is not None:
        avg = np.expand_dims(avg, axis)
    sqr = _ensure_numeric((avg - values)**2)
    np.putmask(sqr, mask, 0)
    result = sqr.sum(axis=axis, dtype=np.float64) / d

    # Return variance as np.float64 (the datatype used in the accumulator),
    # unless we were dealing with a float array, in which case use the same
    # precision as the original values array.
    if is_float_dtype(dtype):
        result = result.astype(dtype)
    return _wrap_results(result, values.dtype)
