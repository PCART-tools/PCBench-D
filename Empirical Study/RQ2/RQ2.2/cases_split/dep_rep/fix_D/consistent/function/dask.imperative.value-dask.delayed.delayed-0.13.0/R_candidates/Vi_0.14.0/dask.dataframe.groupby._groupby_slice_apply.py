def _groupby_slice_apply(df, grouper, key, func):
    # No need to use raise if unaligned here - this is only called after
    # shuffling, which makes everything aligned already
    g = df.groupby(grouper)
    if key:
        g = g[key]
    return g.apply(func)
