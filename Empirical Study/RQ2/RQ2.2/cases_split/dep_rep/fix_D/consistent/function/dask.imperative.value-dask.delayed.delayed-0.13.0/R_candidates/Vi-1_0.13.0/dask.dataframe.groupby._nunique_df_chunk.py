def _nunique_df_chunk(df, *index, **kwargs):
    levels = kwargs.pop('levels')
    name = kwargs.pop('name')

    # we call set_index here to force a possibly duplicate index
    # for our reduce step
    grouped = df.groupby(index)[[name]].apply(pd.DataFrame.drop_duplicates)

    if isinstance(levels, list):
        grouped.index = pd.MultiIndex.from_arrays([
            grouped.index.get_level_values(level=level) for level in levels
        ])
    else:
        grouped.index = grouped.index.get_level_values(level=levels)

    return grouped
