def test_getitem():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                       'B': [9, 8, 7, 6, 5, 4, 3, 2, 1],
                       'C': [True, False, True] * 3},
                      columns=list('ABC'))
    ddf = dd.from_pandas(df, 2)
    assert_eq(ddf['A'], df['A'])
    # check cache consistency
    tm.assert_series_equal(ddf['A']._meta, ddf._meta['A'])

    assert_eq(ddf[['A', 'B']], df[['A', 'B']])
    tm.assert_frame_equal(ddf[['A', 'B']]._meta, ddf._meta[['A', 'B']])

    assert_eq(ddf[ddf.C], df[df.C])
    tm.assert_series_equal(ddf.C._meta, ddf._meta.C)

    assert_eq(ddf[ddf.C.repartition([0, 2, 5, 8])], df[df.C])

    pytest.raises(KeyError, lambda: df['X'])
    pytest.raises(KeyError, lambda: df[['A', 'X']])
    pytest.raises(AttributeError, lambda: df.X)

    # not str/unicode
    df = pd.DataFrame(np.random.randn(10, 5))
    ddf = dd.from_pandas(df, 2)
    assert_eq(ddf[0], df[0])
    assert_eq(ddf[[1, 2]], df[[1, 2]])

    pytest.raises(KeyError, lambda: df[8])
    pytest.raises(KeyError, lambda: df[[1, 8]])
