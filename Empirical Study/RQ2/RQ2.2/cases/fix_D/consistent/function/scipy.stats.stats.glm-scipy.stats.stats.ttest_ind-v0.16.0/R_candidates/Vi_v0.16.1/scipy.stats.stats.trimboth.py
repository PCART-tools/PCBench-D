def trimboth(a, proportiontocut, axis=0):
    """
    Slices off a proportion of items from both ends of an array.

    Slices off the passed proportion of items from both ends of the passed
    array (i.e., with `proportiontocut` = 0.1, slices leftmost 10% **and**
    rightmost 10% of scores).  You must pre-sort the array if you want
    'proper' trimming.  Slices off less if proportion results in a
    non-integer slice index (i.e., conservatively slices off
    `proportiontocut`).

    Parameters
    ----------
    a : array_like
        Data to trim.
    proportiontocut : float
        Proportion (in range 0-1) of total data set to trim of each end.
    axis : int or None, optional
        Axis along which to trim data. Default is 0. If None, compute over
        the whole array `a`.

    Returns
    -------
    out : ndarray
        Trimmed version of array `a`.

    See Also
    --------
    trim_mean

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.arange(20)
    >>> b = stats.trimboth(a, 0.1)
    >>> b.shape
    (16,)

    """
    a = np.asarray(a)
    if axis is None:
        a = a.ravel()
        axis = 0

    nobs = a.shape[axis]
    lowercut = int(proportiontocut * nobs)
    uppercut = nobs - lowercut
    if (lowercut >= uppercut):
        raise ValueError("Proportion too big.")

    sl = [slice(None)] * a.ndim
    sl[axis] = slice(lowercut, uppercut)
    return a[sl]
