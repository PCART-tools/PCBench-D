def test_series_groupby():
    s = pd.Series([1, 2, 2, 1, 1])
    pd_group = s.groupby(s)

    ss = dd.from_pandas(s, npartitions=2)
    dask_group = ss.groupby(ss)

    pd_group2 = s.groupby(s + 1)
    dask_group2 = ss.groupby(ss + 1)

    for dg, pdg in [(dask_group, pd_group), (pd_group2, dask_group2)]:
        assert eq(dg.count(), pdg.count())
        assert eq(dg.sum(), pdg.sum())
        assert eq(dg.min(), pdg.min())
        assert eq(dg.max(), pdg.max())
