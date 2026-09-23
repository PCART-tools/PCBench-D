def set_index_post_series(df, index_name, drop, column_dtype):
    df2 = df.drop('_partitions', axis=1).set_index('_index', drop=True)
    df2.index.name = index_name
    df2.columns = df2.columns.astype(column_dtype)
    return df2
