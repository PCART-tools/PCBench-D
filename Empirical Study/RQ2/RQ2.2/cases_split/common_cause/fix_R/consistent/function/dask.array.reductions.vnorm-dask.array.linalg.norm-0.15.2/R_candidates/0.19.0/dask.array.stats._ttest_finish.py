def _ttest_finish(df, t):
    """Common code between all 3 t-test functions."""
    # XXX: np.abs -> da.absolute
    # XXX: delayed(distributions.t.sf)
    prob = delayed(distributions.t.sf)(da.absolute(t),
                                       df) * 2  # use np.abs to get upper tail
    if t.ndim == 0:
        t = t[()]

    return t, prob
