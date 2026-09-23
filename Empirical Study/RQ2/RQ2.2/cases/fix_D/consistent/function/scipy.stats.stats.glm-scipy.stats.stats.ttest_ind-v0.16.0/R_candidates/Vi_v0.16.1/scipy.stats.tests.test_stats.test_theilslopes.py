def test_theilslopes():
    # Basic slope test.
    slope, intercept, lower, upper = stats.theilslopes([0,1,1])
    assert_almost_equal(slope, 0.5)
    assert_almost_equal(intercept, 0.5)

    # Test of confidence intervals.
    x = [1, 2, 3, 4, 10, 12, 18]
    y = [9, 15, 19, 20, 45, 55, 78]
    slope, intercept, lower, upper = stats.theilslopes(y, x, 0.07)
    assert_almost_equal(slope, 4)
    assert_almost_equal(upper, 4.38, decimal=2)
    assert_almost_equal(lower, 3.71, decimal=2)
