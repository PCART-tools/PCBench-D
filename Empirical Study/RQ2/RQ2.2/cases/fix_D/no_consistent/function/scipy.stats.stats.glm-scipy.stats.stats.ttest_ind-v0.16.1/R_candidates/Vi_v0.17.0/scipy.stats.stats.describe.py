def describe(a, axis=0, ddof=1, bias=True, nan_policy='propagate'):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
       Input data.
    axis : int or None, optional
       Axis along which statistics are calculated. Default is 0.
       If None, compute over the whole array `a`.
    ddof : int, optional
        Delta degrees of freedom (only for variance).  Default is 1.
    bias : bool, optional
        If False, then the skewness and kurtosis calculations are corrected for
        statistical bias.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

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
       Skewness, based on moment calculations with denominator equal to
       the number of observations, i.e. no degrees of freedom correction.
    kurtosis : ndarray or float
       Kurtosis (Fisher).  The kurtosis is normalized so that it is
       zero for the normal distribution.  No degrees of freedom are used.

    See Also
    --------
    skew, kurtosis

    Examples
    --------
    >>> from scipy import stats
    >>> a = np.arange(10)
    >>> stats.describe(a)
    DescribeResult(nobs=10, minmax=(0, 9), mean=4.5, variance=9.1666666666666661,
                   skewness=0.0, kurtosis=-1.2242424242424244)
    >>> b = [[1, 2], [3, 4]]
    >>> stats.describe(b)
    DescribeResult(nobs=2, minmax=(array([1, 2]), array([3, 4])),
                   mean=array([ 2., 3.]), variance=array([ 2., 2.]),
                   skewness=array([ 0., 0.]), kurtosis=array([-2., -2.]))

    """
    a, axis = _chk_asarray(a, axis)

    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        return mstats_basic.describe(a, axis, ddof, bias)

    if contains_nan and nan_policy == 'propagate':
        res = np.zeros(6) * np.nan
        return DescribeResult(*res)

    if a.size == 0:
        raise ValueError("The input must not be empty.")
    n = a.shape[axis]
    mm = (np.min(a, axis=axis), np.max(a, axis=axis))
    m = np.mean(a, axis=axis)
    v = np.var(a, axis=axis, ddof=ddof)
    sk = skew(a, axis, bias=bias)
    kurt = kurtosis(a, axis, bias=bias)

    return DescribeResult(n, mm, m, v, sk, kurt)
