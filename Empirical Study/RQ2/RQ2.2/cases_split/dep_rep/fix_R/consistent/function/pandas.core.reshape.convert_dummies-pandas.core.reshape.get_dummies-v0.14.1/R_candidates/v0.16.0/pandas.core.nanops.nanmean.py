@disallow('M8')
@bottleneck_switch()
def nanmean(values, axis=None, skipna=True):
    values, mask, dtype, dtype_max = _get_values(values, skipna, 0)
    the_sum = _ensure_numeric(values.sum(axis, dtype=dtype_max))
    count = _get_counts(mask, axis)

    if axis is not None and getattr(the_sum, 'ndim', False):
        the_mean = the_sum / count
        ct_mask = count == 0
        if ct_mask.any():
            the_mean[ct_mask] = np.nan
    else:
        the_mean = the_sum / count if count > 0 else np.nan

    return _wrap_results(the_mean, dtype)
