def _apply_chunk(df, index, func, columns):
    if isinstance(df, pd.Series):
        return func(df.groupby(index))
    else:
        columns = columns if isinstance(columns, str) else list(columns)
        return func(df.groupby(index)[columns])
