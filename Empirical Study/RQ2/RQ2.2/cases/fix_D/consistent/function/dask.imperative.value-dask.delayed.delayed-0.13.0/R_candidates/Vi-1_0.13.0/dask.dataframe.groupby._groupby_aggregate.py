def _groupby_aggregate(df, aggfunc=None, levels=None):
    return aggfunc(df.groupby(level=levels, sort=False))
