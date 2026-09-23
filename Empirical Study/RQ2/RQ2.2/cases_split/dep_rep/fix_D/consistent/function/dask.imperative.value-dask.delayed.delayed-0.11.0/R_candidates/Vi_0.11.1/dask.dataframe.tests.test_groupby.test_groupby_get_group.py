def test_groupby_get_group():
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 6], 'b': [4, 2, 7]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 2, 6], 'b': [3, 3, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [4, 3, 7], 'b': [1, 1, 3]},
                                  index=[9, 9, 9])}
    meta = dsk[('x', 0)]
    d = dd.DataFrame(dsk, 'x', meta, [0, 4, 9, 9])
    full = d.compute()

    for ddkey, pdkey in [('b', 'b'), (d.b, full.b),
                         (d.b + 1, full.b + 1)]:
        ddgrouped = d.groupby(ddkey)
        pdgrouped = full.groupby(pdkey)
        # DataFrame
        assert eq(ddgrouped.get_group(2), pdgrouped.get_group(2))
        assert eq(ddgrouped.get_group(3), pdgrouped.get_group(3))
        # Series
        assert eq(ddgrouped.a.get_group(3), pdgrouped.a.get_group(3))
        assert eq(ddgrouped.a.get_group(2), pdgrouped.a.get_group(2))
