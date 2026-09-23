def test_theilslopes():
    # Test for basic slope and intercept.
    slope, intercept, lower, upper = mstats.theilslopes([0,1,1])
    assert_almost_equal(slope, 0.5)
    assert_almost_equal(intercept, 0.5)

    # Test for correct masking.
    y = np.ma.array([0,1,100,1], mask=[False, False, True, False])
    slope, intercept, lower, upper = mstats.theilslopes(y)
    assert_almost_equal(slope, 1./3)
    assert_almost_equal(intercept, 2./3)

    # Test of confidence intervals from example in Sen (1968).
    x = [1, 2, 3, 4, 10, 12, 18]
    y = [9, 15, 19, 20, 45, 55, 78]
    slope, intercept, lower, upper = mstats.theilslopes(y, x, 0.07)
    assert_almost_equal(slope, 4)
    assert_almost_equal(upper, 4.38, decimal=2)
    assert_almost_equal(lower, 3.71, decimal=2)
