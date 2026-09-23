def test_groupby_set_index():
    df = tm.makeTimeDataFrame()
    ddf = dd.from_pandas(df, npartitions=2)
    assert raises(NotImplementedError,
                  lambda: ddf.groupby(df.index.month, as_index=False))
