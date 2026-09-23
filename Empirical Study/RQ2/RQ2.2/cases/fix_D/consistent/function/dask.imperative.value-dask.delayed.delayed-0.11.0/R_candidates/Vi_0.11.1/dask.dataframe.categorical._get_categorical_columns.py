def _get_categorical_columns(df):

    dtypes = df.dtypes
    columns = [name for name, dt in zip(dtypes.index, dtypes.values)
               if is_categorical_dtype(dt)]
    return columns
