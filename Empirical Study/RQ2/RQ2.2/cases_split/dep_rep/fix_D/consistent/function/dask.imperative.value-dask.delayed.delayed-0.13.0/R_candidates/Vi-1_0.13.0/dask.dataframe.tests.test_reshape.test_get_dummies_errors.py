def test_get_dummies_errors():
    with pytest.raises(NotImplementedError):
        # not Categorical
        s = pd.Series([1, 1, 1, 2, 2, 1, 3, 4])
        ds = dd.from_pandas(s, 2)
        dd.get_dummies(ds)
