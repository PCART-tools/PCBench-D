def categorize(df, columns=None, **kwargs):
    """
    Convert columns of dataframe to category dtype

    This aids performance, both in-memory and in spilling to disk
    """
    if columns is None:
        dtypes = df.dtypes
        columns = [name for name, dt in zip(dtypes.index, dtypes.values)
                    if dt == 'O']
    if not isinstance(columns, (list, tuple)):
        columns = [columns]

    distincts = [df[col].drop_duplicates() for col in columns]
    values = compute(*distincts, **kwargs)

    func = partial(_categorize_block, categories=dict(zip(columns, values)))
    return df.map_partitions(func, columns=df.columns)
