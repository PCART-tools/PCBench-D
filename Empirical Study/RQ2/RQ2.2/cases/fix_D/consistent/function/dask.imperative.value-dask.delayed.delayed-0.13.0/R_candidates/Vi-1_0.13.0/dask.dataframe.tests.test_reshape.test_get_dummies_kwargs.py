def test_get_dummies_kwargs():
    s = pd.Series([1, 1, 1, 2, 2, 1, 3, 4], dtype='category')
    exp = pd.get_dummies(s, prefix='X', prefix_sep='-')

    ds = dd.from_pandas(s, 2)
    res = dd.get_dummies(ds, prefix='X', prefix_sep='-')
    assert_eq(res, exp)
    tm.assert_index_equal(res.columns, pd.Index(['X-1', 'X-2', 'X-3', 'X-4']))

    exp = pd.get_dummies(s, drop_first=True)

    ds = dd.from_pandas(s, 2)
    res = dd.get_dummies(ds, drop_first=True)
    assert_eq(res, exp)
    tm.assert_index_equal(res.columns, exp.columns)

    # nan
    s = pd.Series([1, 1, 1, 2, np.nan, 3, np.nan, 5], dtype='category')
    exp = pd.get_dummies(s)

    ds = dd.from_pandas(s, 2)
    res = dd.get_dummies(ds)
    assert_eq(res, exp)
    tm.assert_index_equal(res.columns, exp.columns)

    # dummy_na
    exp = pd.get_dummies(s, dummy_na=True)

    ds = dd.from_pandas(s, 2)
    res = dd.get_dummies(ds, dummy_na=True)
    assert_eq(res, exp)
    tm.assert_index_equal(res.columns, pd.Index([1, 2, 3, 5, np.nan]))

    msg = 'sparse=True is not supported'
    with tm.assertRaisesRegexp(NotImplementedError, msg):
        dd.get_dummies(ds, sparse=True)
