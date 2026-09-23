@np.deprecate(message="stats.threshold is deprecated in scipy 0.17.0")
def threshold(a, threshmin=None, threshmax=None, newval=0):
    """
    Clip array to a given value.

    Similar to numpy.clip(), except that values less than `threshmin` or
    greater than `threshmax` are replaced by `newval`, instead of by
    `threshmin` and `threshmax` respectively.

    Parameters
    ----------
    a : array_like
        Data to threshold.
    threshmin : float, int or None, optional
        Minimum threshold, defaults to None.
    threshmax : float, int or None, optional
        Maximum threshold, defaults to None.
    newval : float or int, optional
        Value to put in place of values in `a` outside of bounds.
        Defaults to 0.

    Returns
    -------
    out : ndarray
        The clipped input array, with values less than `threshmin` or
        greater than `threshmax` replaced with `newval`.

    Examples
    --------
    >>> a = np.array([9, 9, 6, 3, 1, 6, 1, 0, 0, 8])
    >>> from scipy import stats
    >>> stats.threshold(a, threshmin=2, threshmax=8, newval=-1)
    array([-1, -1,  6,  3, -1,  6, -1, -1, -1,  8])

    """
    a = asarray(a).copy()
    mask = zeros(a.shape, dtype=bool)
    if threshmin is not None:
        mask |= (a < threshmin)
    if threshmax is not None:
        mask |= (a > threshmax)
    a[mask] = newval
    return a
