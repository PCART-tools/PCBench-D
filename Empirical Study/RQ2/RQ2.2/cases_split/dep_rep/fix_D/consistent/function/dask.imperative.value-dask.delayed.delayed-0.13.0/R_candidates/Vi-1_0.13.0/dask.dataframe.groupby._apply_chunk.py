def _apply_chunk(df, *index, **kwargs):
    func = kwargs.pop('func')
    columns = kwargs.pop('columns')

    if isinstance(df, pd.Series) or columns is None:
        return func(df.groupby(index))
    else:
        if isinstance(columns, (tuple, list, set, pd.Index)):
            columns = list(columns)
        return func(df.groupby(index)[columns])
