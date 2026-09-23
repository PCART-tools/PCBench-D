def ttest_1samp(a, popmean, axis=0):
    """
    Calculates the T-test for the mean of ONE group of scores.

    Parameters
    ----------
    a : array_like
        sample observation
    popmean : float or array_like
        expected value in null hypothesis, if array_like than it must have the
        same shape as `a` excluding the axis dimension
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        array `a`.

    Returns
    -------
    statistic : float or array
        t-statistic
    pvalue : float or array
        two-tailed p-value

    Notes
    -----
    For more details on `ttest_1samp`, see `stats.ttest_1samp`.

    """
    a, axis = _chk_asarray(a, axis)
    if a.size == 0:
        return (np.nan, np.nan)

    x = a.mean(axis=axis)
    v = a.var(axis=axis, ddof=1)
    n = a.count(axis=axis)
    # force df to be an array for masked division not to throw a warning
    df = ma.asanyarray(n - 1.0)
    svar = ((n - 1.0) * v) / df
    with np.errstate(divide='ignore', invalid='ignore'):
        t = (x - popmean) / ma.sqrt(svar / n)
    prob = special.betainc(0.5*df, 0.5, df/(df + t*t))

    return Ttest_1sampResult(t, prob)
