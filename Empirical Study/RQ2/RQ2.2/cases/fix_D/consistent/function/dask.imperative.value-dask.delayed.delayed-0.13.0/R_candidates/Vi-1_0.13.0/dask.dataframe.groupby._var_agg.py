def _var_agg(g, levels, ddof):
    g = g.groupby(level=levels, sort=False).sum()
    nc = len(g.columns)
    x = g[g.columns[:nc // 3]]
    x2 = g[g.columns[nc // 3:2 * nc // 3]].rename(columns=lambda c: c[:-3])
    n = g[g.columns[-nc // 3:]].rename(columns=lambda c: c[:-6])

    # TODO: replace with _finalize_var?
    result = x2 - x ** 2 / n
    div = (n - ddof)
    div[div < 0] = 0
    result /= div
    result[(n - ddof) == 0] = np.nan
    assert isinstance(result, pd.DataFrame)
    return result
