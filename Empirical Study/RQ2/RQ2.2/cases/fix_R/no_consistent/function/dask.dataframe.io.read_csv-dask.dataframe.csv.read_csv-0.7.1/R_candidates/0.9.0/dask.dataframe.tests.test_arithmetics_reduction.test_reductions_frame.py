def test_reductions_frame():
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 5, 6], 'b': [3, 2, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [7, 8, 9], 'b': [0, 0, 0]},
                                  index=[9, 9, 9])}
    ddf1 = dd.DataFrame(dsk, 'x', ['a', 'b'], [0, 4, 9, 9])
    pdf1 = ddf1.compute()

    assert eq(ddf1.sum(), pdf1.sum())
    assert eq(ddf1.min(), pdf1.min())
    assert eq(ddf1.max(), pdf1.max())
    assert eq(ddf1.count(), pdf1.count())
    assert eq(ddf1.std(), pdf1.std())
    assert eq(ddf1.var(), pdf1.var())
    assert eq(ddf1.std(ddof=0), pdf1.std(ddof=0))
    assert eq(ddf1.var(ddof=0), pdf1.var(ddof=0))
    assert eq(ddf1.mean(), pdf1.mean())

    for axis in [0, 1, 'index', 'columns']:
        assert eq(ddf1.sum(axis=axis), pdf1.sum(axis=axis))
        assert eq(ddf1.min(axis=axis), pdf1.min(axis=axis))
        assert eq(ddf1.max(axis=axis), pdf1.max(axis=axis))
        assert eq(ddf1.count(axis=axis), pdf1.count(axis=axis))
        assert eq(ddf1.std(axis=axis), pdf1.std(axis=axis))
        assert eq(ddf1.var(axis=axis), pdf1.var(axis=axis))
        assert eq(ddf1.std(axis=axis, ddof=0), pdf1.std(axis=axis, ddof=0))
        assert eq(ddf1.var(axis=axis, ddof=0), pdf1.var(axis=axis, ddof=0))
        assert eq(ddf1.mean(axis=axis), pdf1.mean(axis=axis))

    assert raises(ValueError, lambda: ddf1.sum(axis='incorrect').compute())

    # axis=0
    assert_dask_graph(ddf1.sum(), 'dataframe-sum')
    assert_dask_graph(ddf1.min(), 'dataframe-min')
    assert_dask_graph(ddf1.max(), 'dataframe-max')
    assert_dask_graph(ddf1.count(), 'dataframe-count')
    # std, var, mean consists from sum and count operations
    assert_dask_graph(ddf1.std(), 'dataframe-sum')
    assert_dask_graph(ddf1.std(), 'dataframe-count')
    assert_dask_graph(ddf1.var(), 'dataframe-sum')
    assert_dask_graph(ddf1.var(), 'dataframe-count')
    assert_dask_graph(ddf1.mean(), 'dataframe-sum')
    assert_dask_graph(ddf1.mean(), 'dataframe-count')

    # axis=1
    assert_dask_graph(ddf1.sum(axis=1), 'dataframe-sum(axis=1)')
    assert_dask_graph(ddf1.min(axis=1), 'dataframe-min(axis=1)')
    assert_dask_graph(ddf1.max(axis=1), 'dataframe-max(axis=1)')
    assert_dask_graph(ddf1.count(axis=1), 'dataframe-count(axis=1)')
    assert_dask_graph(ddf1.std(axis=1), 'dataframe-std(axis=1, ddof=1)')
    assert_dask_graph(ddf1.var(axis=1), 'dataframe-var(axis=1, ddof=1)')
    assert_dask_graph(ddf1.mean(axis=1), 'dataframe-mean(axis=1)')
