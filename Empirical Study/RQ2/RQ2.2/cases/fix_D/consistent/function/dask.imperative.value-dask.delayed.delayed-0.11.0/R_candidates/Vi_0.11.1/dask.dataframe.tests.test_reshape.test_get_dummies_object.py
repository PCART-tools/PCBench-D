def test_get_dummies_object():
    df = pd.DataFrame({'a': pd.Categorical([1, 2, 3, 4, 4, 3, 2, 1]),
                       'b': list('abcdabcd'),
                       'c': pd.Categorical(list('abcdabcd'))})
    # exclude object columns
    exp = pd.get_dummies(df, columns=['a', 'c'])

    ddf = dd.from_pandas(df, 2)
    res = dd.get_dummies(ddf)
    assert eq(res, exp)
    tm.assert_index_equal(res.columns, exp.columns)

    exp = pd.get_dummies(df, columns=['a'])

    ddf = dd.from_pandas(df, 2)
    res = dd.get_dummies(ddf, columns=['a'])
    assert eq(res, exp)
    tm.assert_index_equal(res.columns, exp.columns)

    # cannot target object columns
    msg = 'target columns must have category dtype'
    with tm.assertRaisesRegexp(ValueError, msg):
        dd.get_dummies(ddf, columns=['b'])
