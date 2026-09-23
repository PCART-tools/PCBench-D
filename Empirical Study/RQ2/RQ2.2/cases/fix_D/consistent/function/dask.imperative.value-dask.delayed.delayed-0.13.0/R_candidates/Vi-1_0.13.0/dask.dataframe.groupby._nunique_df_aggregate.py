def _nunique_df_aggregate(df, levels, name):
    return df.groupby(level=levels, sort=False)[name].nunique()
