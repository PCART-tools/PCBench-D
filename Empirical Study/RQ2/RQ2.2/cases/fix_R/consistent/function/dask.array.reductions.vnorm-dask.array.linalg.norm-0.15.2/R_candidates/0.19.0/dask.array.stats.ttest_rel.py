@doc_wraps(scipy.stats.ttest_rel)
def ttest_rel(a, b, axis=0, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")

    n = a.shape[axis]
    df = float(n - 1)

    d = (a - b).astype(np.float64)
    v = da.var(d, axis, ddof=1)
    dm = da.mean(d, axis)
    denom = da.sqrt(v / float(n))

    with np.errstate(divide='ignore', invalid='ignore'):
        t = da.divide(dm, denom)
    t, prob = _ttest_finish(df, t)

    return delayed(Ttest_relResult, nout=2)(t, prob)
