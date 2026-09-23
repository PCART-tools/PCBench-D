def _nunique_df_combine(df, levels):
    result = df.groupby(level=levels, sort=False).apply(pd.DataFrame.drop_duplicates)

    if isinstance(levels, list):
        result.index = pd.MultiIndex.from_arrays([
            result.index.get_level_values(level=level) for level in levels
        ])
    else:
        result.index = result.index.get_level_values(level=levels)

    return result
