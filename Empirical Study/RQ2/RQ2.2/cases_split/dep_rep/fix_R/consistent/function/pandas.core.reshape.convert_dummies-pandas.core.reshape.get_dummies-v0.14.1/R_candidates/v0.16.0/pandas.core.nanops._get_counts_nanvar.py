def _get_counts_nanvar(mask, axis, ddof):
    count = _get_counts(mask, axis)

    d = count-ddof

    # always return NaN, never inf
    if np.isscalar(count):
        if count <= ddof:
            count = np.nan
            d = np.nan
    else:
        mask2 = count <= ddof
        if mask2.any():
            np.putmask(d, mask2, np.nan)
            np.putmask(count, mask2, np.nan)
    return count, d
