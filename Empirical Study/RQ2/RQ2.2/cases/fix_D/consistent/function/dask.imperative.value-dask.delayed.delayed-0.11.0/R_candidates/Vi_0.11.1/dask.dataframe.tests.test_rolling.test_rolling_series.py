def test_rolling_series():
    for ts in [
            pd.Series(np.random.randn(25).cumsum()),
            pd.Series(np.random.randint(100, size=(25,)))]:
        dts = dd.from_pandas(ts, 3)
        basic_rolling_tests(ts, dts)
