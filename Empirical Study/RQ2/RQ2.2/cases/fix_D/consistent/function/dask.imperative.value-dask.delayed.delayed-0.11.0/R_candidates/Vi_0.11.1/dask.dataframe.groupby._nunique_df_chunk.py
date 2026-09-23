def _nunique_df_chunk(df, index):
    # we call set_index here to force a possibly duplicate index
    # for our reduce step
    grouped = (df.groupby(index).apply(pd.DataFrame.drop_duplicates))
    grouped.index = grouped.index.get_level_values(level=0)
    return grouped
