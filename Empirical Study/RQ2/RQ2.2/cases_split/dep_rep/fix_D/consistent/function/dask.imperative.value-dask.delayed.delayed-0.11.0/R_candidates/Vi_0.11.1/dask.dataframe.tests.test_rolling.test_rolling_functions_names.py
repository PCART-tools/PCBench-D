def test_rolling_functions_names():
    df = pd.DataFrame({'a': [1, 2, 3],
                       'b': [4, 5, 6]})
    a = dd.from_pandas(df, npartitions=2)
    assert sorted(dd.rolling_sum(a, 2).dask) == sorted(dd.rolling_sum(a, 2).dask)
