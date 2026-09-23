def _apply_chunk(df, index, func, columns):
    if isinstance(df, pd.Series):
        return func(df.groupby(index))
    else:
        return func(df.groupby(index)[columns])
