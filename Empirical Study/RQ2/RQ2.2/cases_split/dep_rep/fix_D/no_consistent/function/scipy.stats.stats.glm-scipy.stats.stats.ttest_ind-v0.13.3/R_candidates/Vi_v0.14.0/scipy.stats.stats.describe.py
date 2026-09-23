def describe(a, axis=0):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
       data
    axis : int or None
       axis along which statistics are calculated. If axis is None, then data
       array is raveled. The default axis is zero.

    Returns
    -------
    size of the data : int
       length of data along axis
    (min, max): tuple of ndarrays or floats
       minimum and maximum value of data array
    arithmetic mean : ndarray or float
       mean of data along axis
    unbiased variance : ndarray or float
       variance of the data along axis, denominator is number of observations
       minus one.
    biased skewness : ndarray or float
       skewness, based on moment calculations with denominator equal to the
       number of observations, i.e. no degrees of freedom correction
    biased kurtosis : ndarray or float
       kurtosis (Fisher), the kurtosis is normalized so that it is zero for the
       normal distribution. No degrees of freedom or bias correction is used.

    See Also
    --------
    skew
    kurtosis

    """
    a, axis = _chk_asarray(a, axis)
    n = a.shape[axis]
    mm = (np.min(a, axis=axis), np.max(a, axis=axis))
    m = np.mean(a, axis=axis)
    v = np.var(a, axis=axis, ddof=1)
    sk = skew(a, axis)
    kurt = kurtosis(a, axis)
    return n, mm, m, v, sk, kurt
