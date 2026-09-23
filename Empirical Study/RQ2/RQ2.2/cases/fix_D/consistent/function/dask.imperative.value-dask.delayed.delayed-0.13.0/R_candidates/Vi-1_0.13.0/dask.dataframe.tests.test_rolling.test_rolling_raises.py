def test_rolling_raises():
    df = pd.DataFrame({'a': np.random.randn(25).cumsum(),
                       'b': np.random.randint(100, size=(25,))})
    ddf = dd.from_pandas(df, 3)
    pytest.raises(ValueError, lambda: ddf.rolling(1.5))
    pytest.raises(ValueError, lambda: ddf.rolling(-1))
    pytest.raises(ValueError, lambda: ddf.rolling(3, min_periods=1.2))
    pytest.raises(ValueError, lambda: ddf.rolling(3, min_periods=-2))
    pytest.raises(ValueError, lambda: ddf.rolling(3, axis=10))
    pytest.raises(ValueError, lambda: ddf.rolling(3, axis='coulombs'))
    pytest.raises(NotImplementedError, lambda: ddf.rolling(100).mean().compute())
