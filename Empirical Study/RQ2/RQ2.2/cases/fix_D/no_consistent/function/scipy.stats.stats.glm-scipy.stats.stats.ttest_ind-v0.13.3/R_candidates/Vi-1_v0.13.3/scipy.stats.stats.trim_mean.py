def trim_mean(a, proportiontocut, axis=0):
    """
    Return mean of array after trimming distribution from both lower and upper
    tails.

    If `proportiontocut` = 0.1, slices off 'leftmost' and 'rightmost' 10% of
    scores. Slices off LESS if proportion results in a non-integer slice
    index (i.e., conservatively slices off `proportiontocut` ).

    Parameters
    ----------
    a : array_like
        Input array
    proportiontocut : float
        Fraction to cut off of both tails of the distribution
    axis : int or None, optional
        Axis along which the trimmed means are computed. The default is axis=0.
        If axis is None then the trimmed mean will be computed for the
        flattened array.

    Returns
    -------
    trim_mean : ndarray
        Mean of trimmed array.

    See Also
    --------
    trimboth

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
    newa = trimboth(np.sort(a, axis), proportiontocut, axis=axis)
    return np.mean(newa, axis=axis)
