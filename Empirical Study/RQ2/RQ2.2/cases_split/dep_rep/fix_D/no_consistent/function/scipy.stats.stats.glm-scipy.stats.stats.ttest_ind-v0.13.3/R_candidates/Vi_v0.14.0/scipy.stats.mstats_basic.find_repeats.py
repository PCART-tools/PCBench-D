def find_repeats(arr):
    """Find repeats in arr and return a tuple (repeats, repeat_count).
    Masked values are discarded.

    Parameters
    ----------
    arr : sequence
        Input array. The array is flattened if it is not 1D.

    Returns
    -------
    repeats : ndarray
        Array of repeated values.
    counts : ndarray
        Array of counts.

    """
    marr = ma.compressed(arr)
    if not marr.size:
        return (np.array(0), np.array(0))
    (v1, v2, n) = futil.dfreps(ma.array(ma.compressed(arr), copy=True))
    return (v1[:n], v2[:n])
