def test_reductions():
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 5, 6], 'b': [3, 2, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [7, 8, 9], 'b': [0, 0, 0]},
                                  index=[9, 9, 9])}
    ddf1 = dd.DataFrame(dsk, 'x', ['a', 'b'], [0, 4, 9, 9])
    pdf1 = ddf1.compute()

    nans1 = pd.Series([1] + [np.nan] * 4 + [2] + [np.nan] * 3)
    nands1 = dd.from_pandas(nans1, 2)
    nans2 = pd.Series([1] + [np.nan] * 8)
    nands2 = dd.from_pandas(nans2, 2)
    nans3 = pd.Series([np.nan] * 9)
    nands3 = dd.from_pandas(nans3, 2)

    bools = pd.Series([True, False, True, False, True], dtype=bool)
    boolds = dd.from_pandas(bools, 2)

    for dds, pds in [(ddf1.b, pdf1.b), (ddf1.a, pdf1.a),
                     (ddf1['a'], pdf1['a']), (ddf1['b'], pdf1['b']),
                     (nands1, nans1), (nands2, nans2), (nands3, nans3),
                     (boolds, bools)]:
        assert isinstance(dds, dd.Series)
        assert isinstance(pds, pd.Series)
        assert eq(dds.sum(), pds.sum())
        assert eq(dds.min(), pds.min())
        assert eq(dds.max(), pds.max())
        assert eq(dds.count(), pds.count())
        assert eq(dds.std(), pds.std())
        assert eq(dds.var(), pds.var())
        assert eq(dds.std(ddof=0), pds.std(ddof=0))
        assert eq(dds.var(ddof=0), pds.var(ddof=0))
        assert eq(dds.mean(), pds.mean())
        assert eq(dds.nunique(), pds.nunique())
        assert eq(dds.nbytes, pds.nbytes)

        assert eq(dds.sum(skipna=False), pds.sum(skipna=False))
        assert eq(dds.min(skipna=False), pds.min(skipna=False))
        assert eq(dds.max(skipna=False), pds.max(skipna=False))
        assert eq(dds.std(skipna=False), pds.std(skipna=False))
        assert eq(dds.var(skipna=False), pds.var(skipna=False))
        assert eq(dds.std(skipna=False, ddof=0), pds.std(skipna=False, ddof=0))
        assert eq(dds.var(skipna=False, ddof=0), pds.var(skipna=False, ddof=0))
        assert eq(dds.mean(skipna=False), pds.mean(skipna=False))

    assert_dask_graph(ddf1.b.sum(), 'series-sum')
    assert_dask_graph(ddf1.b.min(), 'series-min')
    assert_dask_graph(ddf1.b.max(), 'series-max')
    assert_dask_graph(ddf1.b.count(), 'series-count')
    assert_dask_graph(ddf1.b.std(), 'series-std(ddof=1)')
    assert_dask_graph(ddf1.b.var(), 'series-var(ddof=1)')
    assert_dask_graph(ddf1.b.std(ddof=0), 'series-std(ddof=0)')
    assert_dask_graph(ddf1.b.var(ddof=0), 'series-var(ddof=0)')
    assert_dask_graph(ddf1.b.mean(), 'series-mean')
    # nunique is performed using drop-duplicates
    assert_dask_graph(ddf1.b.nunique(), 'drop-duplicates')
