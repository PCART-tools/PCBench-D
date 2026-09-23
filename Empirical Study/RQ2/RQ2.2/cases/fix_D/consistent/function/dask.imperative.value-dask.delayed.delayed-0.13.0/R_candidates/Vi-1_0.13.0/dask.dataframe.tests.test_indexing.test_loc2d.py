def test_loc2d():
    # index indexer is always regarded as slice for duplicated values
    assert_eq(d.loc[5, 'a'], full.loc[5:5, 'a'])
    # assert_eq(d.loc[[5], 'a'], full.loc[[5], 'a'])
    assert_eq(d.loc[5, ['a']], full.loc[5:5, ['a']])
    # assert_eq(d.loc[[5], ['a']], full.loc[[5], ['a']])

    assert_eq(d.loc[3:8, 'a'], full.loc[3:8, 'a'])
    assert_eq(d.loc[:8, 'a'], full.loc[:8, 'a'])
    assert_eq(d.loc[3:, 'a'], full.loc[3:, 'a'])

    assert_eq(d.loc[3:8, ['a']], full.loc[3:8, ['a']])
    assert_eq(d.loc[:8, ['a']], full.loc[:8, ['a']])
    assert_eq(d.loc[3:, ['a']], full.loc[3:, ['a']])

    # 3d
    with tm.assertRaises(pd.core.indexing.IndexingError):
        d.loc[3, 3, 3]

    # Series should raise
    with tm.assertRaises(pd.core.indexing.IndexingError):
        d.a.loc[3, 3]

    with tm.assertRaises(pd.core.indexing.IndexingError):
        d.a.loc[3:, 3]

    with tm.assertRaises(pd.core.indexing.IndexingError):
        d.a.loc[d.a % 2 == 0, 3]
