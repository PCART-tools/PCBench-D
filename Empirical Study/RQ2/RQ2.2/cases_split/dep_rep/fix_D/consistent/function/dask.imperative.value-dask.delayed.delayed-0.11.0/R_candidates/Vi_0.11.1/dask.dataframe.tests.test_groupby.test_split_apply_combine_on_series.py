def test_split_apply_combine_on_series():
    pdf1 = pd.DataFrame({'a': [1, 2, 6, 4, 4, 6, 4, 3, 7],
                         'b': [4, 2, 7, 3, 3, 1, 1, 1, 2]},
                        index=[0, 1, 3, 5, 6, 8, 9, 9, 9])
    ddf = dd.from_pandas(pdf1, npartitions=3)
    ddf1 = ddf

    for ddkey, pdkey in [('b', 'b'), (ddf1.b, pdf1.b),
                         (ddf1.b + 1, pdf1.b + 1)]:
        assert eq(ddf1.groupby(ddkey).a.min(), pdf1.groupby(pdkey).a.min())
        assert eq(ddf1.groupby(ddkey).a.max(), pdf1.groupby(pdkey).a.max())
        assert eq(ddf1.groupby(ddkey).a.count(), pdf1.groupby(pdkey).a.count())
        assert eq(ddf1.groupby(ddkey).a.mean(), pdf1.groupby(pdkey).a.mean())
        assert eq(ddf1.groupby(ddkey).a.nunique(), pdf1.groupby(pdkey).a.nunique())
        for ddof in [0, 1, 2]:
            assert eq(ddf1.groupby(ddkey).a.var(ddof),
                      pdf1.groupby(pdkey).a.var(ddof))
            assert eq(ddf1.groupby(ddkey).a.std(ddof),
                      pdf1.groupby(pdkey).a.std(ddof))

        assert eq(ddf1.groupby(ddkey).sum(), pdf1.groupby(pdkey).sum())
        assert eq(ddf1.groupby(ddkey).min(), pdf1.groupby(pdkey).min())
        assert eq(ddf1.groupby(ddkey).max(), pdf1.groupby(pdkey).max())
        assert eq(ddf1.groupby(ddkey).count(), pdf1.groupby(pdkey).count())
        assert eq(ddf1.groupby(ddkey).mean(), pdf1.groupby(pdkey).mean())
        for ddof in [0, 1, 2]:
            assert eq(ddf1.groupby(ddkey).var(ddof),
                      pdf1.groupby(pdkey).var(ddof), check_dtype=False)
            assert eq(ddf1.groupby(ddkey).std(ddof),
                      pdf1.groupby(pdkey).std(ddof), check_dtype=False)

    for ddkey, pdkey in [(ddf1.b, pdf1.b), (ddf1.b + 1, pdf1.b + 1)]:
        assert eq(ddf1.a.groupby(ddkey).sum(), pdf1.a.groupby(pdkey).sum(), check_names=False)
        assert eq(ddf1.a.groupby(ddkey).max(), pdf1.a.groupby(pdkey).max(), check_names=False)
        assert eq(ddf1.a.groupby(ddkey).count(), pdf1.a.groupby(pdkey).count(), check_names=False)
        assert eq(ddf1.a.groupby(ddkey).mean(), pdf1.a.groupby(pdkey).mean(), check_names=False)
        assert eq(ddf1.a.groupby(ddkey).nunique(), pdf1.a.groupby(pdkey).nunique(), check_names=False)
        for ddof in [0, 1, 2]:
            assert eq(ddf1.a.groupby(ddkey).var(ddof),
                      pdf1.a.groupby(pdkey).var(ddof))
            assert eq(ddf1.a.groupby(ddkey).std(ddof),
                      pdf1.a.groupby(pdkey).std(ddof))

    for i in range(8):
        assert eq(ddf1.groupby(ddf1.b > i).a.sum(), pdf1.groupby(pdf1.b > i).a.sum())
        assert eq(ddf1.groupby(ddf1.b > i).a.min(), pdf1.groupby(pdf1.b > i).a.min())
        assert eq(ddf1.groupby(ddf1.b > i).a.max(), pdf1.groupby(pdf1.b > i).a.max())
        assert eq(ddf1.groupby(ddf1.b > i).a.count(), pdf1.groupby(pdf1.b > i).a.count())
        assert eq(ddf1.groupby(ddf1.b > i).a.mean(), pdf1.groupby(pdf1.b > i).a.mean())
        assert eq(ddf1.groupby(ddf1.b > i).a.nunique(), pdf1.groupby(pdf1.b > i).a.nunique())

        assert eq(ddf1.groupby(ddf1.a > i).b.sum(), pdf1.groupby(pdf1.a > i).b.sum())
        assert eq(ddf1.groupby(ddf1.a > i).b.min(), pdf1.groupby(pdf1.a > i).b.min())
        assert eq(ddf1.groupby(ddf1.a > i).b.max(), pdf1.groupby(pdf1.a > i).b.max())
        assert eq(ddf1.groupby(ddf1.a > i).b.count(), pdf1.groupby(pdf1.a > i).b.count())
        assert eq(ddf1.groupby(ddf1.a > i).b.mean(), pdf1.groupby(pdf1.a > i).b.mean())
        assert eq(ddf1.groupby(ddf1.a > i).b.nunique(), pdf1.groupby(pdf1.a > i).b.nunique())

        assert eq(ddf1.groupby(ddf1.b > i).sum(), pdf1.groupby(pdf1.b > i).sum())
        assert eq(ddf1.groupby(ddf1.b > i).min(), pdf1.groupby(pdf1.b > i).min())
        assert eq(ddf1.groupby(ddf1.b > i).max(), pdf1.groupby(pdf1.b > i).max())
        assert eq(ddf1.groupby(ddf1.b > i).count(), pdf1.groupby(pdf1.b > i).count())
        assert eq(ddf1.groupby(ddf1.b > i).mean(), pdf1.groupby(pdf1.b > i).mean())

        assert eq(ddf1.groupby(ddf1.a > i).sum(), pdf1.groupby(pdf1.a > i).sum())
        assert eq(ddf1.groupby(ddf1.a > i).min(), pdf1.groupby(pdf1.a > i).min())
        assert eq(ddf1.groupby(ddf1.a > i).max(), pdf1.groupby(pdf1.a > i).max())
        assert eq(ddf1.groupby(ddf1.a > i).count(), pdf1.groupby(pdf1.a > i).count())
        assert eq(ddf1.groupby(ddf1.a > i).mean(), pdf1.groupby(pdf1.a > i).mean())

        for ddof in [0, 1, 2]:
            assert eq(ddf1.groupby(ddf1.b > i).std(ddof),
                      pdf1.groupby(pdf1.b > i).std(ddof))

    for ddkey, pdkey in [('a', 'a'), (ddf1.a, pdf1.a),
                         (ddf1.a + 1, pdf1.a + 1), (ddf1.a > 3, pdf1.a > 3)]:
        assert eq(ddf1.groupby(ddkey).b.sum(), pdf1.groupby(pdkey).b.sum())
        assert eq(ddf1.groupby(ddkey).b.min(), pdf1.groupby(pdkey).b.min())
        assert eq(ddf1.groupby(ddkey).b.max(), pdf1.groupby(pdkey).b.max())
        assert eq(ddf1.groupby(ddkey).b.count(), pdf1.groupby(pdkey).b.count())
        assert eq(ddf1.groupby(ddkey).b.mean(), pdf1.groupby(pdkey).b.mean())
        assert eq(ddf1.groupby(ddkey).b.nunique(), pdf1.groupby(pdkey).b.nunique())

        assert eq(ddf1.groupby(ddkey).sum(), pdf1.groupby(pdkey).sum())
        assert eq(ddf1.groupby(ddkey).min(), pdf1.groupby(pdkey).min())
        assert eq(ddf1.groupby(ddkey).max(), pdf1.groupby(pdkey).max())
        assert eq(ddf1.groupby(ddkey).count(), pdf1.groupby(pdkey).count())
        assert eq(ddf1.groupby(ddkey).mean(), pdf1.groupby(pdkey).mean().astype(float))

        for ddof in [0, 1, 2]:
            assert eq(ddf1.groupby(ddkey).b.std(ddof),
                      pdf1.groupby(pdkey).b.std(ddof))

    assert sorted(ddf1.groupby('b').a.sum().dask) == \
           sorted(ddf1.groupby('b').a.sum().dask)
    assert sorted(ddf1.groupby(ddf1.a > 3).b.mean().dask) == \
           sorted(ddf1.groupby(ddf1.a > 3).b.mean().dask)

    # test raises with incorrect key
    assert raises(KeyError, lambda: ddf1.groupby('x'))
    assert raises(KeyError, lambda: ddf1.groupby(['a', 'x']))
    assert raises(KeyError, lambda: ddf1.groupby('a')['x'])
    assert raises(KeyError, lambda: ddf1.groupby('a')['b', 'x'])
    assert raises(KeyError, lambda: ddf1.groupby('a')[['b', 'x']])

    # test graph node labels
    assert_dask_graph(ddf1.groupby('b').a.sum(), 'series-groupby-sum')
    assert_dask_graph(ddf1.groupby('b').a.min(), 'series-groupby-min')
    assert_dask_graph(ddf1.groupby('b').a.max(), 'series-groupby-max')
    assert_dask_graph(ddf1.groupby('b').a.count(), 'series-groupby-count')
    assert_dask_graph(ddf1.groupby('b').a.var(), 'series-groupby-var')
    # mean consists from sum and count operations
    assert_dask_graph(ddf1.groupby('b').a.mean(), 'series-groupby-sum')
    assert_dask_graph(ddf1.groupby('b').a.mean(), 'series-groupby-count')
    assert_dask_graph(ddf1.groupby('b').a.nunique(), 'series-groupby-nunique')

    assert_dask_graph(ddf1.groupby('b').sum(), 'dataframe-groupby-sum')
    assert_dask_graph(ddf1.groupby('b').min(), 'dataframe-groupby-min')
    assert_dask_graph(ddf1.groupby('b').max(), 'dataframe-groupby-max')
    assert_dask_graph(ddf1.groupby('b').count(), 'dataframe-groupby-count')
    # mean consists from sum and count operations
    assert_dask_graph(ddf1.groupby('b').mean(), 'dataframe-groupby-sum')
    assert_dask_graph(ddf1.groupby('b').mean(), 'dataframe-groupby-count')
