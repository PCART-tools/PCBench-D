def _nunique_df_chunk(df, *index, **kwargs):
    levels = kwargs.pop('levels')
    name = kwargs.pop('name')

    g = _groupby_raise_unaligned(df, by=index)
    grouped = g[[name]].apply(pd.DataFrame.drop_duplicates)

    # we set the index here to force a possibly duplicate index
    # for our reduce step
    if isinstance(levels, list):
        grouped.index = pd.MultiIndex.from_arrays([
            grouped.index.get_level_values(level=level) for level in levels
        ])
    else:
        grouped.index = grouped.index.get_level_values(level=levels)

    return grouped
