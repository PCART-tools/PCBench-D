def _update_columns(df: DataFrame, new_columns: Sequence[str]) -> DataFrame:
    if df.width > len(new_columns):
        cols = df.columns
        for i, name in enumerate(new_columns):
            cols[i] = name
        new_columns = cols
    df.columns = list(new_columns)
    return df
