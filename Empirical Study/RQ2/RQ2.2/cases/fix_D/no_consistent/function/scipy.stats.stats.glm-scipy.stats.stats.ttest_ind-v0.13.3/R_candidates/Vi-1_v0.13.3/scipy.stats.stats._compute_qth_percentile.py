def _compute_qth_percentile(sorted, per, interpolation_method, axis):
    if not np.isscalar(per):
        return [_compute_qth_percentile(sorted, i, interpolation_method, axis)
             for i in per]

    if (per < 0) or (per > 100):
        raise ValueError("percentile must be in the range [0, 100]")

    indexer = [slice(None)] * sorted.ndim
    idx = per / 100. * (sorted.shape[axis] - 1)

    if int(idx) != idx:
        # round fractional indices according to interpolation method
        if interpolation_method == 'lower':
            idx = int(np.floor(idx))
        elif interpolation_method == 'higher':
            idx = int(np.ceil(idx))
        elif interpolation_method == 'fraction':
            pass  # keep idx as fraction and interpolate
        else:
            raise ValueError("interpolation_method can only be 'fraction', "
                             "'lower' or 'higher'")

    i = int(idx)
    if i == idx:
        indexer[axis] = slice(i, i + 1)
        weights = array(1)
        sumval = 1.0
    else:
        indexer[axis] = slice(i, i + 2)
        j = i + 1
        weights = array([(j - idx), (idx - i)], float)
        wshape = [1] * sorted.ndim
        wshape[axis] = 2
        weights.shape = wshape
        sumval = weights.sum()

    # Use np.add.reduce to coerce data type
    return np.add.reduce(sorted[indexer] * weights, axis=axis) / sumval
