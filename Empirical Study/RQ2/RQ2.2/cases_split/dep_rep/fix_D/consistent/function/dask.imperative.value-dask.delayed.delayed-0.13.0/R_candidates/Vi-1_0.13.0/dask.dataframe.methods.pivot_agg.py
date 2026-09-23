def pivot_agg(df):
    return df.groupby(level=0).sum()
