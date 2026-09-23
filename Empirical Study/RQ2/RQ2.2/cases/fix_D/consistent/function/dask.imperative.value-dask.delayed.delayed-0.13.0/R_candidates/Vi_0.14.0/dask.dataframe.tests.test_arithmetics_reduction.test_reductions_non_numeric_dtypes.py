def test_reductions_non_numeric_dtypes():
    # test non-numric blocks

    def check_raises(d, p, func):
        pytest.raises((TypeError, ValueError),
                      lambda: getattr(d, func)().compute())
        pytest.raises((TypeError, ValueError),
                      lambda: getattr(p, func)())

    pds = pd.Series(['a', 'b', 'c', 'd', 'e'])
    dds = dd.from_pandas(pds, 2)
    assert_eq(dds.sum(), pds.sum())
    check_raises(dds, pds, 'prod')
    assert_eq(dds.min(), pds.min())
    assert_eq(dds.max(), pds.max())
    assert_eq(dds.count(), pds.count())
    check_raises(dds, pds, 'std')
    check_raises(dds, pds, 'var')
    check_raises(dds, pds, 'sem')
    check_raises(dds, pds, 'mean')
    assert_eq(dds.nunique(), pds.nunique())

    for pds in [pd.Series(pd.Categorical([1, 2, 3, 4, 5], ordered=True)),
                pd.Series(pd.Categorical(list('abcde'), ordered=True)),
                pd.Series(pd.date_range('2011-01-01', freq='D', periods=5))]:
        dds = dd.from_pandas(pds, 2)

        check_raises(dds, pds, 'sum')
        check_raises(dds, pds, 'prod')
        assert_eq(dds.min(), pds.min())
        assert_eq(dds.max(), pds.max())
        assert_eq(dds.count(), pds.count())
        check_raises(dds, pds, 'std')
        check_raises(dds, pds, 'var')
        check_raises(dds, pds, 'sem')
        check_raises(dds, pds, 'mean')
        assert_eq(dds.nunique(), pds.nunique())

    pds = pd.Series(pd.timedelta_range('1 days', freq='D', periods=5))
    dds = dd.from_pandas(pds, 2)
    assert_eq(dds.sum(), pds.sum())
    assert_eq(dds.min(), pds.min())
    assert_eq(dds.max(), pds.max())
    assert_eq(dds.count(), pds.count())

    # ToDo: pandas supports timedelta std, otherwise dask raises:
    # incompatible type for a datetime/timedelta operation [__pow__]
    # assert_eq(dds.std(), pds.std())
    # assert_eq(dds.var(), pds.var())

    # ToDo: pandas supports timedelta std, otherwise dask raises:
    # TypeError: unsupported operand type(s) for *: 'float' and 'Timedelta'
    # assert_eq(dds.mean(), pds.mean())

    assert_eq(dds.nunique(), pds.nunique())
