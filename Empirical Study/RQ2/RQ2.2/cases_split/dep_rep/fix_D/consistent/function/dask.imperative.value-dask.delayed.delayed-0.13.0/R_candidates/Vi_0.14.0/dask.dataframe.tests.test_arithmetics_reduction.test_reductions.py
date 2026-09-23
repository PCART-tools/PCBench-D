@pytest.mark.parametrize('split_every', [False, 2])
def test_reductions(split_every):
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 5, 6], 'b': [3, 2, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [7, 8, 9], 'b': [0, 0, 0]},
                                  index=[9, 9, 9])}
    meta = make_meta({'a': 'i8', 'b': 'i8'}, index=pd.Index([], 'i8'))
    ddf1 = dd.DataFrame(dsk, 'x', meta, [0, 4, 9, 9])
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
        assert_eq(dds.sum(split_every=split_every), pds.sum())
        assert_eq(dds.prod(split_every=split_every), pds.prod())
        assert_eq(dds.min(split_every=split_every), pds.min())
        assert_eq(dds.max(split_every=split_every), pds.max())
        assert_eq(dds.count(split_every=split_every), pds.count())
        assert_eq(dds.std(split_every=split_every), pds.std())
        assert_eq(dds.var(split_every=split_every), pds.var())
        assert_eq(dds.sem(split_every=split_every), pds.sem())
        assert_eq(dds.std(ddof=0, split_every=split_every), pds.std(ddof=0))
        assert_eq(dds.var(ddof=0, split_every=split_every), pds.var(ddof=0))
        assert_eq(dds.sem(ddof=0, split_every=split_every), pds.sem(ddof=0))
        assert_eq(dds.mean(split_every=split_every), pds.mean())
        assert_eq(dds.nunique(split_every=split_every), pds.nunique())

        assert_eq(dds.sum(skipna=False, split_every=split_every),
                  pds.sum(skipna=False))
        assert_eq(dds.prod(skipna=False, split_every=split_every),
                  pds.prod(skipna=False))
        assert_eq(dds.min(skipna=False, split_every=split_every),
                  pds.min(skipna=False))
        assert_eq(dds.max(skipna=False, split_every=split_every),
                  pds.max(skipna=False))
        assert_eq(dds.std(skipna=False, split_every=split_every),
                  pds.std(skipna=False))
        assert_eq(dds.var(skipna=False, split_every=split_every),
                  pds.var(skipna=False))
        assert_eq(dds.sem(skipna=False, split_every=split_every),
                  pds.sem(skipna=False))
        assert_eq(dds.std(skipna=False, ddof=0, split_every=split_every),
                  pds.std(skipna=False, ddof=0))
        assert_eq(dds.var(skipna=False, ddof=0, split_every=split_every),
                  pds.var(skipna=False, ddof=0))
        assert_eq(dds.sem(skipna=False, ddof=0, split_every=split_every),
                  pds.sem(skipna=False, ddof=0))
        assert_eq(dds.mean(skipna=False, split_every=split_every),
                  pds.mean(skipna=False))

    assert_dask_graph(ddf1.b.sum(split_every=split_every), 'series-sum')
    assert_dask_graph(ddf1.b.prod(split_every=split_every), 'series-prod')
    assert_dask_graph(ddf1.b.min(split_every=split_every), 'series-min')
    assert_dask_graph(ddf1.b.max(split_every=split_every), 'series-max')
    assert_dask_graph(ddf1.b.count(split_every=split_every), 'series-count')
    assert_dask_graph(ddf1.b.std(split_every=split_every), 'series-std')
    assert_dask_graph(ddf1.b.var(split_every=split_every), 'series-var')
    assert_dask_graph(ddf1.b.sem(split_every=split_every), 'series-sem')
    assert_dask_graph(ddf1.b.std(ddof=0, split_every=split_every), 'series-std')
    assert_dask_graph(ddf1.b.var(ddof=0, split_every=split_every), 'series-var')
    assert_dask_graph(ddf1.b.sem(ddof=0, split_every=split_every), 'series-sem')
    assert_dask_graph(ddf1.b.mean(split_every=split_every), 'series-mean')
    # nunique is performed using drop-duplicates
    assert_dask_graph(ddf1.b.nunique(split_every=split_every), 'drop-duplicates')

    assert_eq(ddf1.index.min(split_every=split_every), pdf1.index.min())
    assert_eq(ddf1.index.max(split_every=split_every), pdf1.index.max())
    assert_eq(ddf1.index.count(split_every=split_every), pd.notnull(pdf1.index).sum())
