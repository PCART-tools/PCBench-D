def test_groupby_index_array():
    df = tm.makeTimeDataFrame()
    ddf = dd.from_pandas(df, npartitions=2)

    eq(df.A.groupby(df.index.month).nunique(),
       ddf.A.groupby(ddf.index.month).nunique(), check_names=False)
