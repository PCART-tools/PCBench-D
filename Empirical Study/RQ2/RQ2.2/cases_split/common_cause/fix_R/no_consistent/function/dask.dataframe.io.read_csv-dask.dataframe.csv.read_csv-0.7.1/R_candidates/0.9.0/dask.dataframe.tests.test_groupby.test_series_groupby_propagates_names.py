def test_series_groupby_propagates_names():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    ddf = dd.from_pandas(df, 2)
    func = lambda df: df['y'].sum()

    result = ddf.groupby('x').apply(func, columns='y')

    expected = df.groupby('x').apply(func)
    expected.name = 'y'
    assert eq(result, expected)
