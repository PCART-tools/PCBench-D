def _groupby_slice_apply(df, grouper, key, func):
    g = df.groupby(grouper)
    if key:
        g = g[key]
    return g.apply(func)
