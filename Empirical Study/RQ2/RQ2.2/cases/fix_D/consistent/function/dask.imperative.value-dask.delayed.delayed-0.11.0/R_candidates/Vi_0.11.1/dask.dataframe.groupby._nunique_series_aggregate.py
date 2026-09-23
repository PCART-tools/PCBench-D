def _nunique_series_aggregate(df):
    return df.groupby(df.columns[1])[df.columns[0]].nunique()
