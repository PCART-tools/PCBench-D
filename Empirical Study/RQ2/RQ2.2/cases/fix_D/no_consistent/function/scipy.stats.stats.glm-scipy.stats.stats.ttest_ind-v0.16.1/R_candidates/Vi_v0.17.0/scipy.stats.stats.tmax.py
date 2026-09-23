def tmax(a, upperlimit=None, axis=0, inclusive=True, nan_policy='propagate'):
    """
    Compute the trimmed maximum

    This function computes the maximum value of an array along a given axis,
    while ignoring values larger than a specified upper limit.

    Parameters
    ----------
    a : array_like
        array of values
    upperlimit : None or float, optional
        Values in the input array greater than the given limit will be ignored.
        When upperlimit is None, then all values are used. The default value
        is None.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over the
        whole array `a`.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the upper limit
        are included.  The default value is True.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    tmax : float, int or ndarray

    Examples
    --------
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmax(x)
    19

    >>> stats.tmax(x, 13)
    13

    >>> stats.tmax(x, 13, inclusive=False)
    12

    """
    a, axis = _chk_asarray(a, axis)
    am = _mask_to_limits(a, (None, upperlimit), (False, inclusive))

    contains_nan, nan_policy = _contains_nan(am, nan_policy)

    if contains_nan and nan_policy == 'omit':
        am = ma.masked_invalid(am)

    res = ma.maximum.reduce(am, axis).data
    if res.ndim == 0:
        return res[()]
    return res
