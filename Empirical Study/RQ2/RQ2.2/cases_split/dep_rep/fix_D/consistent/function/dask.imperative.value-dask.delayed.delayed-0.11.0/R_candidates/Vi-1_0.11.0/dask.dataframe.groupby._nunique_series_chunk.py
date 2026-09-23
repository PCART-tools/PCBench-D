def _nunique_series_chunk(df, index):
    assert isinstance(df, pd.Series)
    if isinstance(index, np.ndarray):
        assert len(index) == len(df)
        index = pd.Series(index, index=df.index)
    grouped = pd.concat([df, index], axis=1).drop_duplicates()
    return grouped
