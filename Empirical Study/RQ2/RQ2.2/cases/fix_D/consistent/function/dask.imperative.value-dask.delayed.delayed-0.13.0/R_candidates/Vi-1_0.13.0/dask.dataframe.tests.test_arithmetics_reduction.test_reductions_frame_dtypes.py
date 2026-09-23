def test_reductions_frame_dtypes():
    df = pd.DataFrame({'int': [1, 2, 3, 4, 5, 6, 7, 8],
                       'float': [1., 2., 3., 4., np.nan, 6., 7., 8.],
                       'dt': [pd.NaT] + [datetime(2011, i, 1) for i in range(1, 8)],
                       'str': list('abcdefgh')})
    ddf = dd.from_pandas(df, 3)
    assert_eq(df.sum(), ddf.sum())
    assert_eq(df.prod(), ddf.prod())
    assert_eq(df.min(), ddf.min())
    assert_eq(df.max(), ddf.max())
    assert_eq(df.count(), ddf.count())
    assert_eq(df.std(), ddf.std())
    assert_eq(df.var(), ddf.var())
    assert_eq(df.sem(), ddf.sem())
    assert_eq(df.std(ddof=0), ddf.std(ddof=0))
    assert_eq(df.var(ddof=0), ddf.var(ddof=0))
    assert_eq(df.sem(ddof=0), ddf.sem(ddof=0))
    assert_eq(df.mean(), ddf.mean())

    assert_eq(df._get_numeric_data(), ddf._get_numeric_data())

    numerics = ddf[['int', 'float']]
    assert numerics._get_numeric_data().dask == numerics.dask
