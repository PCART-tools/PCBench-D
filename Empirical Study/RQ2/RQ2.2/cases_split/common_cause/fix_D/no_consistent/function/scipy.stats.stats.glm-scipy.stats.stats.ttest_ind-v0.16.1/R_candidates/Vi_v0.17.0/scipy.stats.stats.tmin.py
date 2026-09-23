def tmin(a, lowerlimit=None, axis=0, inclusive=True, nan_policy='propagate'):
    """
    Compute the trimmed minimum

    This function finds the miminum value of an array `a` along the
    specified axis, but only considering values greater than a specified
    lower limit.

    Parameters
    ----------
    a : array_like
        array of values
    lowerlimit : None or float, optional
        Values in the input array less than the given limit will be ignored.
        When lowerlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the lower limit
        are included.  The default value is True.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    tmin : float, int or ndarray

    Examples
    --------
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmin(x)
    0

    >>> stats.tmin(x, 13)
    13

    >>> stats.tmin(x, 13, inclusive=False)
    14

    """
    a, axis = _chk_asarray(a, axis)
    am = _mask_to_limits(a, (lowerlimit, None), (inclusive, False))

    contains_nan, nan_policy = _contains_nan(am, nan_policy)

    if contains_nan and nan_policy == 'omit':
        am = ma.masked_invalid(am)

    res = ma.minimum.reduce(am, axis).data
    if res.ndim == 0:
        return res[()]
    return res
