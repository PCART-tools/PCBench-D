def rolling_functions_tests(p, d):
    # Old-fashioned rolling API
    assert_eq(pd.rolling_count(p, 3), dd.rolling_count(d, 3))
    assert_eq(pd.rolling_sum(p, 3), dd.rolling_sum(d, 3))
    assert_eq(pd.rolling_mean(p, 3), dd.rolling_mean(d, 3))
    assert_eq(pd.rolling_median(p, 3), dd.rolling_median(d, 3))
    assert_eq(pd.rolling_min(p, 3), dd.rolling_min(d, 3))
    assert_eq(pd.rolling_max(p, 3), dd.rolling_max(d, 3))
    assert_eq(pd.rolling_std(p, 3), dd.rolling_std(d, 3))
    assert_eq(pd.rolling_var(p, 3), dd.rolling_var(d, 3))
    # see note around test_rolling_dataframe for logic concerning precision
    assert_eq(pd.rolling_skew(p, 3),
              dd.rolling_skew(d, 3), check_less_precise=True)
    assert_eq(pd.rolling_kurt(p, 3),
              dd.rolling_kurt(d, 3), check_less_precise=True)
    assert_eq(pd.rolling_quantile(p, 3, 0.5), dd.rolling_quantile(d, 3, 0.5))
    assert_eq(pd.rolling_apply(p, 3, mad), dd.rolling_apply(d, 3, mad))
    assert_eq(pd.rolling_window(p, 3, win_type='boxcar'),
              dd.rolling_window(d, 3, win_type='boxcar'))
    # Test with edge-case window sizes
    assert_eq(pd.rolling_sum(p, 0), dd.rolling_sum(d, 0))
    assert_eq(pd.rolling_sum(p, 1), dd.rolling_sum(d, 1))
    # Test with kwargs
    assert_eq(pd.rolling_sum(p, 3, min_periods=3),
              dd.rolling_sum(d, 3, min_periods=3))
