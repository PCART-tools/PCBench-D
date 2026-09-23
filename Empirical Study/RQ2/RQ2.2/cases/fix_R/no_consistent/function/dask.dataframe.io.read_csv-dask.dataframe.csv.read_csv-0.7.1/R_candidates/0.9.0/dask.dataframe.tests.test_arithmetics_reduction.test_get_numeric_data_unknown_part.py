def test_get_numeric_data_unknown_part():
    df = pd.DataFrame({'a': range(5), 'b': range(5), 'c': list('abcde')})
    ddf = dd.from_pandas(df, 3)
    # Drop dtype information
    ddf = dd.DataFrame(ddf.dask, ddf._name, ['a', 'b', 'c'], ddf.divisions)
    assert eq(ddf._get_numeric_data(), df._get_numeric_data())
