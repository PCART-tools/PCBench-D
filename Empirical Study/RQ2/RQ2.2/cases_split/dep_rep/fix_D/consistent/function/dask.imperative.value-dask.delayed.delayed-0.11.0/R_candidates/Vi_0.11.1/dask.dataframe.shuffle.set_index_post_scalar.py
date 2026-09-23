def set_index_post_scalar(df, index_name, drop, column_dtype):
    df2 = df.drop('_partitions', axis=1).set_index(index_name, drop=drop)
    df2.columns = df2.columns.astype(column_dtype)
    return df2
