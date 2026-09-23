def _drop_unnamed_null_columns(df: pl.DataFrame) -> pl.DataFrame:
    """If DataFrame contains unnamed columns that contain only nulls, drop them."""
    null_cols = []
    for col_name in df.columns:
        # note that if multiple unnamed columns are found then all but
        # the first one will be ones will be named as "_duplicated_{n}"
        if col_name == "" or re.match(r"_duplicated_\d+$", col_name):
            if df[col_name].null_count() == len(df):
                null_cols.append(col_name)
    if null_cols:
        df = df.drop(*null_cols)
    return df
