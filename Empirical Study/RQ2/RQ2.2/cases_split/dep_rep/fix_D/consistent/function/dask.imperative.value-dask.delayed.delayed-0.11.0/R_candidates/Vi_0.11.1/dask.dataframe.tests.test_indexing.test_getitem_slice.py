def test_getitem_slice():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                       'B': [9, 8, 7, 6, 5, 4, 3, 2, 1],
                       'C': [True, False, True] * 3},
                      index=list('abcdefghi'))
    ddf = dd.from_pandas(df, 3)
    assert eq(ddf['a':'e'], df['a':'e'])
    assert eq(ddf['a':'b'], df['a':'b'])
    assert eq(ddf['f':], df['f':])
