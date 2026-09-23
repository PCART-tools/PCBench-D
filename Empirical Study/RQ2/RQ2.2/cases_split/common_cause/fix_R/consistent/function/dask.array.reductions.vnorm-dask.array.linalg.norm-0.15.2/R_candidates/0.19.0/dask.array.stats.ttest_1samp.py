@doc_wraps(scipy.stats.ttest_1samp)
def ttest_1samp(a, popmean, axis=0, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")
    n = a.shape[axis]
    df = n - 1

    d = da.mean(a, axis) - popmean
    v = da.var(a, axis, ddof=1)
    denom = da.sqrt(v / float(n))

    with np.errstate(divide='ignore', invalid='ignore'):
        t = da.divide(d, denom)
    t, prob = _ttest_finish(df, t)
    return delayed(Ttest_1sampResult, nout=2)(t, prob)
