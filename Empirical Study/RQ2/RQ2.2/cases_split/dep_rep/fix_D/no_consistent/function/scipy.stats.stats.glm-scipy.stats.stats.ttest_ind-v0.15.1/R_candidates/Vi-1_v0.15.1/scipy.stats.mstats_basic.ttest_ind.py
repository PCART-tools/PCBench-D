def ttest_ind(a, b, axis=0):
    a, b, axis = _chk2_asarray(a, b, axis)
    if a.size == 0 or b.size == 0:
        return (np.nan, np.nan)

    (x1, x2) = (a.mean(axis), b.mean(axis))
    (v1, v2) = (a.var(axis=axis, ddof=1), b.var(axis=axis, ddof=1))
    (n1, n2) = (a.count(axis), b.count(axis))
    df = n1 + n2 - 2.
    svar = ((n1-1)*v1+(n2-1)*v2) / df
    t = (x1-x2)/ma.sqrt(svar*(1.0/n1 + 1.0/n2))  # n-D computation here!
    t = ma.filled(t, 1)           # replace NaN t-values with 1.0
    probs = betai(0.5 * df, 0.5, df/(df + t*t)).reshape(t.shape)
    return t, probs.squeeze()
