def drop_columns(df, columns, dtype):
    df = df.drop(columns, axis=1)
    df.columns = df.columns.astype(dtype)
    return df
