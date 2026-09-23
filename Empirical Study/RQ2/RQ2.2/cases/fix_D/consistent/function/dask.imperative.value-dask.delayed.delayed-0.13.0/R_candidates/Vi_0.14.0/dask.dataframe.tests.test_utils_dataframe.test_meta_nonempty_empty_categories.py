def test_meta_nonempty_empty_categories():
    for dtype in ['O', 'f8', 'M8']:
        # Index
        idx = pd.CategoricalIndex([], pd.Index([], dtype=dtype),
                                  ordered=True, name='foo')
        res = meta_nonempty(idx)
        assert type(res) is pd.CategoricalIndex
        assert type(res.categories) is type(idx.categories)
        assert res.ordered == idx.ordered
        assert res.name == idx.name
        # Series
        s = idx.to_series()
        res = meta_nonempty(s)
        assert res.dtype == s.dtype
        assert type(res.cat.categories) is type(s.cat.categories)
        assert res.cat.ordered == s.cat.ordered
        assert res.name == s.name
