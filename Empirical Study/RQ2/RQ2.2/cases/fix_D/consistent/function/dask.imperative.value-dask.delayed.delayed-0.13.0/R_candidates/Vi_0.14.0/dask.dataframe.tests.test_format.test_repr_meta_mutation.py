def test_repr_meta_mutation():
    # Check that the repr changes when meta changes
    df = pd.DataFrame({'a': range(5),
                       'b': ['a', 'b', 'c', 'd', 'e']})
    ddf = dd.from_pandas(df, npartitions=2)
    s1 = repr(ddf)
    assert repr(ddf) == s1
    ddf.b = ddf.b.astype('category')
    assert repr(ddf) != s1
