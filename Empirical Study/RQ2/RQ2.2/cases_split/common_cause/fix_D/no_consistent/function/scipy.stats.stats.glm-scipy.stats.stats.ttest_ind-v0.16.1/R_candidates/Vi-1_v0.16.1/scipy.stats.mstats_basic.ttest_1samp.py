def ttest_1samp(a, popmean, axis=0):
    a, axis = _chk_asarray(a, axis)
    if a.size == 0:
        return (np.nan, np.nan)

    x = a.mean(axis=axis)
    v = a.var(axis=axis, ddof=1)
    n = a.count(axis=axis)
    df = n - 1.
    svar = ((n - 1) * v) / df
    t = (x - popmean) / ma.sqrt(svar / n)
    prob = betai(0.5 * df, 0.5, df / (df + t*t))

    return Ttest_1sampResult(t, prob)
