def _nunique_df_aggregate(df, name):
    return df.groupby(level=0)[name].nunique()
