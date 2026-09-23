def ttest_rel(a, b, axis=0):
    """
    Calculates the T-test on TWO RELATED samples of scores, a and b.

    This is a two-sided test for the null hypothesis that 2 related or
    repeated samples have identical average (expected) values.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape.
    axis : int, optional, (default axis=0)
        Axis can equal None (ravel array first), or an integer (the axis
        over which to operate on a and b).

    Returns
    -------
    t : float or array
        t-statistic
    prob : float or array
        two-tailed p-value

    Notes
    -----
    Examples for the use are scores of the same set of student in
    different exams, or repeated sampling from the same units. The
    test measures whether the average score differs significantly
    across samples (e.g. exams). If we observe a large p-value, for
    example greater than 0.05 or 0.1 then we cannot reject the null
    hypothesis of identical average scores. If the p-value is smaller
    than the threshold, e.g. 1%, 5% or 10%, then we reject the null
    hypothesis of equal averages. Small p-values are associated with
    large t-statistics.

    References
    ----------
    http://en.wikipedia.org/wiki/T-test#Dependent_t-test

    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(12345678) # fix random seed to get same numbers

    >>> rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
    >>> rvs2 = (stats.norm.rvs(loc=5,scale=10,size=500) +
    ...         stats.norm.rvs(scale=0.2,size=500))
    >>> stats.ttest_rel(rvs1,rvs2)
    (0.24101764965300962, 0.80964043445811562)
    >>> rvs3 = (stats.norm.rvs(loc=8,scale=10,size=500) +
    ...         stats.norm.rvs(scale=0.2,size=500))
    >>> stats.ttest_rel(rvs1,rvs3)
    (-3.9995108708727933, 7.3082402191726459e-005)

    """
    a, b, axis = _chk2_asarray(a, b, axis)
    if a.shape[axis] != b.shape[axis]:
        raise ValueError('unequal length arrays')

    if a.size == 0 or b.size == 0:
        return (np.nan, np.nan)

    n = a.shape[axis]
    df = float(n - 1)

    d = (a - b).astype(np.float64)
    v = np.var(d, axis, ddof=1)
    dm = np.mean(d, axis)
    denom = np.sqrt(v / float(n))

    t = np.divide(dm, denom)
    t, prob = _ttest_finish(df, t)

    return t, prob
