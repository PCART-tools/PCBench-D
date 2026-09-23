def test_rolling_functions_raises():
    df = pd.DataFrame({'a': np.random.randn(25).cumsum(),
                       'b': np.random.randint(100, size=(25,))})
    ddf = dd.from_pandas(df, 3)
    assert raises(TypeError, lambda: dd.rolling_mean(ddf, 1.5))
    assert raises(ValueError, lambda: dd.rolling_mean(ddf, -1))
    assert raises(NotImplementedError, lambda: dd.rolling_mean(ddf, 3, freq=2))
    assert raises(NotImplementedError, lambda: dd.rolling_mean(ddf, 3, how='min'))
