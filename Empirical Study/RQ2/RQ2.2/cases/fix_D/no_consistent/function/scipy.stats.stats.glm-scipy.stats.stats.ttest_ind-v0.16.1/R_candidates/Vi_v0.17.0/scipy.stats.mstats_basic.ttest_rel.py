def ttest_rel(a, b, axis=0):
    """
    Calculates the T-test on TWO RELATED samples of scores, a and b.

    Parameters
    ----------
    a, b : array_like
        The arrays must have the same shape.
    axis : int or None, optional
        Axis along which to compute test. If None, compute over the whole
        arrays, `a`, and `b`.

    Returns
    -------
    statistic : float or array
        t-statistic
    pvalue : float or array
        two-tailed p-value

    Notes
    -----
    For more details on `ttest_rel`, see `stats.ttest_rel`.

    """
    a, b, axis = _chk2_asarray(a, b, axis)
    if len(a) != len(b):
        raise ValueError('unequal length arrays')

    if a.size == 0 or b.size == 0:
        return Ttest_relResult(np.nan, np.nan)

    n = a.count(axis)
    df = ma.asanyarray(n-1.0)
    d = (a-b).astype('d')
    dm = d.mean(axis)
    v = d.var(axis=axis, ddof=1)
    denom = ma.sqrt(v / n)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = dm / denom

    probs = special.betainc(0.5*df, 0.5, df/(df + t*t)).reshape(t.shape).squeeze()

    return Ttest_relResult(t, probs)
