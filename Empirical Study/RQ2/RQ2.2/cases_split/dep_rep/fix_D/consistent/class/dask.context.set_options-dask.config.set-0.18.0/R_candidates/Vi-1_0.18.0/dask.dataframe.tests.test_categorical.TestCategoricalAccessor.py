class TestCategoricalAccessor:

    @pytest.mark.parametrize('series', cat_series)
    @pytest.mark.parametrize('prop, compare', [
        ('categories', assert_array_index_eq),
        ('ordered', assert_eq),
        ('codes', assert_array_index_eq)
    ])
    def test_properties(self, series, prop, compare):
        s, ds = series
        expected = getattr(get_cat(s), prop)
        result = getattr(get_cat(ds), prop)
        compare(result, expected)

    @pytest.mark.parametrize('series', cat_series)
    @pytest.mark.parametrize('method, kwargs', [
        ('add_categories', dict(new_categories=['d', 'e'])),
        ('as_ordered', {}),
        ('as_unordered', {}),
        ('as_ordered', {}),
        ('remove_categories', dict(removals=['a'])),
        ('rename_categories', dict(new_categories=['d', 'e', 'f'])),
        ('reorder_categories', dict(new_categories=['a', 'b', 'c'])),
        ('set_categories', dict(new_categories=['a', 'e', 'b'])),
        ('remove_unused_categories', {}),
    ])
    def test_callable(self, series, method, kwargs):
        op = operator.methodcaller(method, **kwargs)

        # Series
        s, ds = series
        expected = op(get_cat(s))
        result = op(get_cat(ds))
        assert_eq(result, expected)
        assert_eq(get_cat(result._meta).categories, get_cat(expected).categories)
        assert_eq(get_cat(result._meta).ordered, get_cat(expected).ordered)

    def test_categorical_empty(self):
        # GH 1705

        def make_empty():
            return pd.DataFrame({"A": pd.Categorical([np.nan, np.nan])})

        def make_full():
            return pd.DataFrame({"A": pd.Categorical(['a', 'a'])})

        a = dd.from_delayed([dask.delayed(make_empty)(),
                             dask.delayed(make_full)()])
        # Used to raise an IndexError
        a.A.cat.categories

    @pytest.mark.parametrize('series', cat_series)
    def test_unknown_categories(self, series):
        a, da = series
        assert da.cat.known
        da = da.cat.as_unknown()
        assert not da.cat.known

        with pytest.raises(NotImplementedError):
            da.cat.categories
        with pytest.raises(NotImplementedError):
            da.cat.codes

        db = da.cat.set_categories(['a', 'b', 'c'])
        assert db.cat.known
        tm.assert_index_equal(db.cat.categories, get_cat(a).categories)
        assert_array_index_eq(db.cat.codes, get_cat(a).codes)

        db = da.cat.as_known()
        assert db.cat.known
        res = db.compute()
        tm.assert_index_equal(db.cat.categories, get_cat(res).categories)
        assert_array_index_eq(db.cat.codes, get_cat(res).codes)

    def test_categorical_string_ops(self):
        a = pd.Series(['a', 'a', 'b'], dtype='category')
        da = dd.from_pandas(a, 2)
        result = da.str.upper()
        expected = a.str.upper()
        assert_eq(result, expected)

    def test_categorical_non_string_raises(self):
        a = pd.Series([1, 2, 3], dtype='category')
        da = dd.from_pandas(a, 2)
        with pytest.raises(AttributeError):
            da.str.upper()
