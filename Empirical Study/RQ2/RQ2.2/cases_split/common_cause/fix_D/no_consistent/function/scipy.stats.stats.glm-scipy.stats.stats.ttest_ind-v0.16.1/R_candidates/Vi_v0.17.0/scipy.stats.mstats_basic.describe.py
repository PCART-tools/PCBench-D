def describe(a, axis=0, ddof=0, bias=True):
    """
    Computes several descriptive statistics of the passed array.

    Parameters
    ----------
    a : array_like
        Data array
    axis : int or None, optional
        Axis along which to calculate statistics. Default 0. If None,
        compute over the whole array `a`.
    ddof : int, optional
        degree of freedom (default 0); note that default ddof is different
        from the same routine in stats.describe
    bias : bool, optional
        If False, then the skewness and kurtosis calculations are corrected for
        statistical bias.

    Returns
    -------
    nobs : int
        (size of the data (discarding missing values)

    minmax : (int, int)
        min, max

    mean : float
        arithmetic mean

    variance : float
        unbiased variance

    skewness : float
        biased skewness

    kurtosis : float
        biased kurtosis

    Examples
    --------
    >>> from scipy.stats.mstats import describe
    >>> ma = np.ma.array(range(6), mask=[0, 0, 0, 1, 1, 1])
    >>> describe(ma)
    DescribeResult(nobs=array(3), minmax=(masked_array(data = 0,
                 mask = False,
           fill_value = 999999)
    , masked_array(data = 2,
                 mask = False,
           fill_value = 999999)
    ), mean=1.0, variance=0.66666666666666663, skewness=masked_array(data = 0.0,
                 mask = False,
           fill_value = 1e+20)
    , kurtosis=-1.5)

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis)
    mm = (ma.minimum.reduce(a), ma.maximum.reduce(a))
    m = a.mean(axis)
    v = a.var(axis, ddof=ddof)
    sk = skew(a, axis, bias=bias)
    kurt = kurtosis(a, axis, bias=bias)

    return DescribeResult(n, mm, m, v, sk, kurt)
