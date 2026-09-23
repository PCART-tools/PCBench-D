def sem(a, axis=0, ddof=1):
    """
    Calculates the standard error of the mean of the input array.

    Also sometimes called standard error of measurement.

    Parameters
    ----------
    a : array_like
        An array containing the values for which the standard error is
        returned.
    axis : int or None, optional
        If axis is None, ravel `a` first. If axis is an integer, this will be
        the axis over which to operate. Defaults to 0.
    ddof : int, optional
        Delta degrees-of-freedom. How many degrees of freedom to adjust
        for bias in limited samples relative to the population estimate
        of variance. Defaults to 1.

    Returns
    -------
    s : ndarray or float
        The standard error of the mean in the sample(s), along the input axis.

    Notes
    -----
    The default value for `ddof` changed in scipy 0.15.0 to be consistent with
    `stats.sem` as well as with the most common definition used (like in the R
    documentation).

    Examples
    --------
    Find standard error along the first axis:

    >>> from scipy import stats
    >>> a = np.arange(20).reshape(5,4)
    >>> print(stats.mstats.sem(a))
    [2.8284271247461903 2.8284271247461903 2.8284271247461903
     2.8284271247461903]

    Find standard error across the whole array, using n degrees of freedom:

    >>> print(stats.mstats.sem(a, axis=None, ddof=0))
    1.2893796958227628

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    s = a.std(axis=axis, ddof=ddof) / ma.sqrt(n)
    return s
