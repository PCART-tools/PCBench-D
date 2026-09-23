def wrap_df(df: PyDataFrame) -> DataFrame:
    return pl.DataFrame._from_pydf(df)
