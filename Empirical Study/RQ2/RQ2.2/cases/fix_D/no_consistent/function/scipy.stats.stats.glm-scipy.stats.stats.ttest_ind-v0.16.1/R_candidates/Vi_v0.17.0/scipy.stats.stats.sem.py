def sem(a, axis=0, ddof=1, nan_policy='propagate'):
    """
    Calculates the standard error of the mean (or standard error of
    measurement) of the values in the input array.

    Parameters
    ----------
    a : array_like
        An array containing the values for which the standard error is
        returned.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    ddof : int, optional
        Delta degrees-of-freedom. How many degrees of freedom to adjust
        for bias in limited samples relative to the population estimate
        of variance. Defaults to 1.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    s : ndarray or float
        The standard error of the mean in the sample(s), along the input axis.

    Notes
    -----
    The default value for `ddof` is different to the default (0) used by other
    ddof containing routines, such as np.std nd stats.nanstd.

    Examples
    --------
    Find standard error along the first axis:

    >>> from scipy import stats
    >>> a = np.arange(20).reshape(5,4)
    >>> stats.sem(a)
    array([ 2.8284,  2.8284,  2.8284,  2.8284])

    Find standard error across the whole array, using n degrees of freedom:

    >>> stats.sem(a, axis=None, ddof=0)
    1.2893796958227628

    """
    a, axis = _chk_asarray(a, axis)

    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        return mstats_basic.sem(a, axis, ddof)

    if contains_nan and nan_policy == 'propagate':
        return np.nan

    n = a.shape[axis]
    s = np.std(a, axis=axis, ddof=ddof) / np.sqrt(n)
    return s
