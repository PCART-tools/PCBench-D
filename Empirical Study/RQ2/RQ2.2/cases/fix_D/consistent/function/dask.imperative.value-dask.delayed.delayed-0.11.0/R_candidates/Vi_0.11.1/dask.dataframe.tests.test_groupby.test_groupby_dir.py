def test_groupby_dir():
    df = pd.DataFrame({'a': range(10), 'b c d e': range(10)})
    ddf = dd.from_pandas(df, npartitions=2)
    g = ddf.groupby('a')
    assert 'a' in dir(g)
    assert 'b c d e' not in dir(g)
