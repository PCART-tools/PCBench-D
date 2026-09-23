def test_series_groupby_errors():
    s = pd.Series([1, 2, 2, 1, 1])

    ss = dd.from_pandas(s, npartitions=2)

    msg = "Grouper for '1' not 1-dimensional"
    with tm.assertRaisesRegexp(ValueError, msg):
        s.groupby([1, 2])    # pandas
    with tm.assertRaisesRegexp(ValueError, msg):
        ss.groupby([1, 2])   # dask should raise the same error
    msg = "Grouper for '2' not 1-dimensional"
    with tm.assertRaisesRegexp(ValueError, msg):
        s.groupby([2])    # pandas
    with tm.assertRaisesRegexp(ValueError, msg):
        ss.groupby([2])   # dask should raise the same error

    msg = "No group keys passed!"
    with tm.assertRaisesRegexp(ValueError, msg):
        s.groupby([])    # pandas
    with tm.assertRaisesRegexp(ValueError, msg):
        ss.groupby([])   # dask should raise the same error

    sss = dd.from_pandas(s, npartitions=3)
    assert raises(NotImplementedError, lambda: ss.groupby(sss))

    with tm.assertRaises(KeyError):
        s.groupby('x')    # pandas
    with tm.assertRaises(KeyError):
        ss.groupby('x')   # dask should raise the same error
