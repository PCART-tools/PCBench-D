def _nunique_series_chunk(df, *index, **_ignored_):
    # convert series to data frame, then hand over to dataframe code path
    assert isinstance(df, pd.Series)

    df = df.to_frame()
    kwargs = dict(name=df.columns[0], levels=_determine_levels(index))
    return _nunique_df_chunk(df, *index, **kwargs)
