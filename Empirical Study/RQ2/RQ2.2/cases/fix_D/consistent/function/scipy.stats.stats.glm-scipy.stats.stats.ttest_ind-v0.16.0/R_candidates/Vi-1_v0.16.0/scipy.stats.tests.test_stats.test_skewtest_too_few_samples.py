def test_skewtest_too_few_samples():
    # Regression test for ticket #1492.
    # skewtest requires at least 8 samples; 7 should raise a ValueError.
    x = np.arange(7.0)
    assert_raises(ValueError, stats.skewtest, x)
