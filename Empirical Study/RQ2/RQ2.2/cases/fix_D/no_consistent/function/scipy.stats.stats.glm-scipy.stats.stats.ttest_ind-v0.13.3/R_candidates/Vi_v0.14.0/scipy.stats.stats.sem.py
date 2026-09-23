def sem(a, axis=0, ddof=1):
    """
    Calculates the standard error of the mean (or standard error of
    measurement) of the values in the input array.

    Parameters
    ----------
    a : array_like
        An array containing the values for which the standard error is
        returned.
    axis : int or None, optional.
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
    n = a.shape[axis]
    s = np.std(a,axis=axis, ddof=ddof) / np.sqrt(n)  # JP check normalization
    return s
