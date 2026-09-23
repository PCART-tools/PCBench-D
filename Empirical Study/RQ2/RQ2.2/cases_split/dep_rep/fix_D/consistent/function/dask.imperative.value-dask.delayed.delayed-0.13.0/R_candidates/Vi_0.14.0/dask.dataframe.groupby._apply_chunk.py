def _apply_chunk(df, *index, **kwargs):
    func = kwargs.pop('chunk')
    columns = kwargs.pop('columns')

    g = _groupby_raise_unaligned(df, by=index)

    if isinstance(df, pd.Series) or columns is None:
        return func(g)
    else:
        if isinstance(columns, (tuple, list, set, pd.Index)):
            columns = list(columns)
        return func(g[columns])
