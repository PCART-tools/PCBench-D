@np.deprecate(message="mstats.threshold is deprecated in scipy 0.17.0")
def threshold(a, threshmin=None, threshmax=None, newval=0):
    """
    Clip array to a given value.

    Similar to numpy.clip(), except that values less than `threshmin` or
    greater than `threshmax` are replaced by `newval`, instead of by
    `threshmin` and `threshmax` respectively.

    Parameters
    ----------
    a : ndarray
        Input data
    threshmin : {None, float}, optional
        Lower threshold. If None, set to the minimum value.
    threshmax : {None, float}, optional
        Upper threshold. If None, set to the maximum value.
    newval : {0, float}, optional
        Value outside the thresholds.

    Returns
    -------
    threshold : ndarray
        Returns `a`, with values less then `threshmin` and values greater
        `threshmax` replaced with `newval`.

    """
    a = ma.array(a, copy=True)
    mask = np.zeros(a.shape, dtype=bool)
    if threshmin is not None:
        mask |= (a < threshmin).filled(False)

    if threshmax is not None:
        mask |= (a > threshmax).filled(False)

    a[mask] = newval
    return a
