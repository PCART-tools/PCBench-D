def test_groupby_multilevel_agg():
    df = pd.DataFrame({'a': [1, 2, 3, 1, 2, 3],
                       'b': [1, 2, 1, 4, 2, 1],
                       'c': [1, 3, 2, 1, 1, 2],
                       'd': [1, 2, 1, 1, 2, 2]})
    ddf = dd.from_pandas(df, 2)

    sol = df.groupby(['a']).mean()
    res = ddf.groupby(['a']).mean()
    assert eq(res, sol)

    sol = df.groupby(['a', 'c']).mean()
    res = ddf.groupby(['a', 'c']).mean()
    assert eq(res, sol)
