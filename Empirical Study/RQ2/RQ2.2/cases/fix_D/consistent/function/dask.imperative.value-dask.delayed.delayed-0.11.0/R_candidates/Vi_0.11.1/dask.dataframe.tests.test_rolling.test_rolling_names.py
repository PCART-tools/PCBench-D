def test_rolling_names():
    df = pd.DataFrame({'a': [1, 2, 3],
                       'b': [4, 5, 6]})
    a = dd.from_pandas(df, npartitions=2)
    assert sorted(a.rolling(2).sum().dask) == sorted(a.rolling(2).sum().dask)
