def _var_chunk(df, *index):
    if isinstance(df, pd.Series):
        df = df.to_frame()
    g = df.groupby(index)
    x = g.sum()
    x2 = g.agg(lambda x: (x**2).sum()).rename(columns=lambda c: c + '-x2')
    n = g.count().rename(columns=lambda c: c + '-count')
    return pd.concat([x, x2, n], axis=1)
