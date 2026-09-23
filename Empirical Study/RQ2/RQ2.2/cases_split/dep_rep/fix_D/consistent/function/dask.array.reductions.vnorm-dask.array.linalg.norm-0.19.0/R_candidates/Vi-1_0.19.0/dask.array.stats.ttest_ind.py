@doc_wraps(scipy.stats.ttest_ind)
def ttest_ind(a, b, axis=0, equal_var=True):
    v1 = da.var(a, axis, ddof=1)  # XXX: np -> da
    v2 = da.var(b, axis, ddof=1)  # XXX: np -> da
    n1 = a.shape[axis]
    n2 = b.shape[axis]

    if equal_var:
        df, denom = _equal_var_ttest_denom(v1, n1, v2, n2)
    else:
        df, denom = _unequal_var_ttest_denom(v1, n1, v2, n2)

    res = _ttest_ind_from_stats(da.mean(a, axis), da.mean(b, axis), denom, df)

    return delayed(Ttest_indResult, nout=2)(*res)
