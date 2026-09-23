def test_groupby_multilevel_getitem():
    df = pd.DataFrame({'a': [1, 2, 3, 1, 2, 3],
                       'b': [1, 2, 1, 4, 2, 1],
                       'c': [1, 3, 2, 1, 1, 2],
                       'd': [1, 2, 1, 1, 2, 2]})
    ddf = dd.from_pandas(df, 2)

    cases = [(ddf.groupby('a')['b'], df.groupby('a')['b']),
             (ddf.groupby(['a', 'b']), df.groupby(['a', 'b'])),
             (ddf.groupby(['a', 'b'])['c'], df.groupby(['a', 'b'])['c']),
             (ddf.groupby('a')[['b', 'c']], df.groupby('a')[['b', 'c']]),
             (ddf.groupby('a')[['b']], df.groupby('a')[['b']]),
             (ddf.groupby(['a', 'b', 'c']), df.groupby(['a', 'b', 'c']))]

    for d, p in cases:
        assert isinstance(d, dd.groupby._GroupBy)
        assert isinstance(p, pd.core.groupby.GroupBy)
        assert eq(d.sum(), p.sum())
        assert eq(d.min(), p.min())
        assert eq(d.max(), p.max())
        assert eq(d.count(), p.count())
        assert eq(d.mean(), p.mean().astype(float))
