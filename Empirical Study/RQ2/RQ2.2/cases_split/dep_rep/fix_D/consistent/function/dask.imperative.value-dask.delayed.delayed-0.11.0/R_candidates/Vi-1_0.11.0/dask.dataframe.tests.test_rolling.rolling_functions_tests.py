def rolling_functions_tests(p, d):
    # Old-fashioned rolling API
    eq(pd.rolling_count(p, 3), dd.rolling_count(d, 3))
    eq(pd.rolling_sum(p, 3), dd.rolling_sum(d, 3))
    eq(pd.rolling_mean(p, 3), dd.rolling_mean(d, 3))
    eq(pd.rolling_median(p, 3), dd.rolling_median(d, 3))
    eq(pd.rolling_min(p, 3), dd.rolling_min(d, 3))
    eq(pd.rolling_max(p, 3), dd.rolling_max(d, 3))
    eq(pd.rolling_std(p, 3), dd.rolling_std(d, 3))
    eq(pd.rolling_var(p, 3), dd.rolling_var(d, 3))
    # see note around test_rolling_dataframe for logic concerning precision
    eq(pd.rolling_skew(p, 3), dd.rolling_skew(d, 3), check_less_precise=True)
    eq(pd.rolling_kurt(p, 3), dd.rolling_kurt(d, 3), check_less_precise=True)
    eq(pd.rolling_quantile(p, 3, 0.5), dd.rolling_quantile(d, 3, 0.5))
    eq(pd.rolling_apply(p, 3, mad), dd.rolling_apply(d, 3, mad))
    with ignoring(ImportError):
        eq(pd.rolling_window(p, 3, 'boxcar'), dd.rolling_window(d, 3, 'boxcar'))
    # Test with edge-case window sizes
    eq(pd.rolling_sum(p, 0), dd.rolling_sum(d, 0))
    eq(pd.rolling_sum(p, 1), dd.rolling_sum(d, 1))
    # Test with kwargs
    eq(pd.rolling_sum(p, 3, min_periods=3), dd.rolling_sum(d, 3, min_periods=3))
