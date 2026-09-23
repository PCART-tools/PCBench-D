def basic_rolling_tests(p, d): # Works for series or df
    # New rolling API
    eq(p.rolling(3).count(), d.rolling(3).count())
    eq(p.rolling(3).sum(), d.rolling(3).sum())
    eq(p.rolling(3).mean(), d.rolling(3).mean())
    eq(p.rolling(3).median(), d.rolling(3).median())
    eq(p.rolling(3).min(), d.rolling(3).min())
    eq(p.rolling(3).max(), d.rolling(3).max())
    eq(p.rolling(3).std(), d.rolling(3).std())
    eq(p.rolling(3).var(), d.rolling(3).var())
    # see note around test_rolling_dataframe for logic concerning precision
    eq(p.rolling(3).skew(), d.rolling(3).skew(), check_less_precise=True)
    eq(p.rolling(3).kurt(), d.rolling(3).kurt(), check_less_precise=True)
    eq(p.rolling(3).quantile(0.5), d.rolling(3).quantile(0.5))
    eq(p.rolling(3).apply(mad), d.rolling(3).apply(mad))
    with ignoring(ImportError):
        eq(p.rolling(3, win_type='boxcar').sum(),
           d.rolling(3, win_type='boxcar').sum())
    # Test with edge-case window sizes
    eq(p.rolling(0).sum(), d.rolling(0).sum())
    eq(p.rolling(1).sum(), d.rolling(1).sum())
    # Test with kwargs
    eq(p.rolling(3, min_periods=2).sum(), d.rolling(3, min_periods=2).sum())
    # Test with center
    eq(p.rolling(3, center=True).max(), d.rolling(3, center=True).max())
    eq(p.rolling(3, center=False).std(), d.rolling(3, center=False).std())
    eq(p.rolling(6, center=True).var(), d.rolling(6, center=True).var())
    # see note around test_rolling_dataframe for logic concerning precision
    eq(p.rolling(7, center=True).skew(), d.rolling(7, center=True).skew(),
                 check_less_precise=True)
