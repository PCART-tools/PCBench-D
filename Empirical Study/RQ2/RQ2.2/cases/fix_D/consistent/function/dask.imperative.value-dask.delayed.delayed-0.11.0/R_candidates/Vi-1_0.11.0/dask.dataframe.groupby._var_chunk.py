def _var_chunk(df, index):
    if isinstance(df, pd.Series):
        df = df.to_frame()
    x = df.groupby(index).sum()
    x2 = (df**2).rename(columns=lambda c: c + '-x2')
    cols = [c + '-x2' for c in x.columns]
    x2 = pd.concat([df, x2], axis=1).groupby(index)[cols].sum()
    n = (df.groupby(index).count()
           .rename(columns=lambda c: c + '-count'))

    result = pd.concat([x, x2, n], axis=1)
    return result
