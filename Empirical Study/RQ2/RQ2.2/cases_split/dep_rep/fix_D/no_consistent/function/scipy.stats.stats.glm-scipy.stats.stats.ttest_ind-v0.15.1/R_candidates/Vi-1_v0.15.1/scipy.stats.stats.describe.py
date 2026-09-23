def describe(a, axis=0, ddof=1):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
       Input data.
    axis : int, optional
       Axis along which statistics are calculated.  If axis is None, then data
       array is raveled.  The default axis is zero.
    ddof : int, optional
        Delta degrees of freedom.  Default is 1.

    Returns
    -------
    nobs : int
       Number of observations (length of data along `axis`).
    minmax: tuple of ndarrays or floats
       Minimum and maximum value of data array.
    mean : ndarray or float
       Arithmetic mean of data along axis.
    variance : ndarray or float
       Unbiased variance of the data along axis, denominator is number of
       observations minus one.
    skewness : ndarray or float
       Biased skewness, based on moment calculations with denominator equal to
       the number of observations, i.e. no degrees of freedom correction.
    kurtosis : ndarray or float
       Biased kurtosis (Fisher).  The kurtosis is normalized so that it is
       zero for the normal distribution.  No degrees of freedom or bias
       correction is used.

    See Also
    --------
    skew, kurtosis

    """
    a, axis = _chk_asarray(a, axis)
    n = a.shape[axis]
    mm = (np.min(a, axis=axis), np.max(a, axis=axis))
    m = np.mean(a, axis=axis)
    v = np.var(a, axis=axis, ddof=ddof)
    sk = skew(a, axis)
    kurt = kurtosis(a, axis)

    # Return namedtuple for clarity
    return _DescribeResult(n, mm, m, v, sk, kurt)
