def test_rolling_functions_series():
    ts = pd.Series(np.random.randn(25).cumsum())
    dts = dd.from_pandas(ts, 3)
    rolling_functions_tests(ts, dts)
