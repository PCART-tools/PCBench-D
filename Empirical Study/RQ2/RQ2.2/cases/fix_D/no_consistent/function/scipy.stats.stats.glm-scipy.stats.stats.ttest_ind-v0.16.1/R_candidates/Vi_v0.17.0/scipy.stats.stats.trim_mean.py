def trim_mean(a, proportiontocut, axis=0):
    """
    Return mean of array after trimming distribution from both tails.

    If `proportiontocut` = 0.1, slices off 'leftmost' and 'rightmost' 10% of
    scores. The input is sorted before slicing. Slices off less if proportion
    results in a non-integer slice index (i.e., conservatively slices off
    `proportiontocut` ).

    Parameters
    ----------
    a : array_like
        Input array
    proportiontocut : float
        Fraction to cut off of both tails of the distribution
    axis : int or None, optional
        Axis along which the trimmed means are computed. Default is 0.
        If None, compute over the whole array `a`.

    Returns
    -------
    trim_mean : ndarray
        Mean of trimmed array.

    See Also
    --------
    trimboth
    tmean : compute the trimmed mean ignoring values outside given `limits`.

    Examples
    --------
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.trim_mean(x, 0.1)
    9.5
    >>> x2 = x.reshape(5, 4)
    >>> x2
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15],
           [16, 17, 18, 19]])
    >>> stats.trim_mean(x2, 0.25)
    array([  8.,   9.,  10.,  11.])
    >>> stats.trim_mean(x2, 0.25, axis=1)
    array([  1.5,   5.5,   9.5,  13.5,  17.5])

    """
    a = np.asarray(a)

    if a.size == 0:
        return np.nan

    if axis is None:
        a = a.ravel()
        axis = 0

    nobs = a.shape[axis]
    lowercut = int(proportiontocut * nobs)
    uppercut = nobs - lowercut
    if (lowercut > uppercut):
        raise ValueError("Proportion too big.")

    # np.partition is preferred but it only exist in numpy 1.8.0 and higher,
    # in those cases we use np.sort
    try:
        atmp = np.partition(a, (lowercut, uppercut - 1), axis)
    except AttributeError:
        atmp = np.sort(a, axis)

    sl = [slice(None)] * atmp.ndim
    sl[axis] = slice(lowercut, uppercut)
    return np.mean(atmp[sl], axis=axis)
