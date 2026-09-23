def test_get_dummies_errors():
    with pytest.raises(NotImplementedError):
        # not Categorical
        s = pd.Series([1, 1, 1, 2, 2, 1, 3, 4])
        ds = dd.from_pandas(s, 2)
        dd.get_dummies(ds)

    # unknown categories
    df = pd.DataFrame({'x': list('abcbc'), 'y': list('bcbcb')})
    ddf = dd.from_pandas(df, npartitions=2)
    ddf._meta = make_meta({'x': 'category', 'y': 'category'})

    with pytest.raises(NotImplementedError):
        dd.get_dummies(ddf)

    with pytest.raises(NotImplementedError):
        dd.get_dummies(ddf, columns=['x', 'y'])

    with pytest.raises(NotImplementedError):
        dd.get_dummies(ddf.x)
