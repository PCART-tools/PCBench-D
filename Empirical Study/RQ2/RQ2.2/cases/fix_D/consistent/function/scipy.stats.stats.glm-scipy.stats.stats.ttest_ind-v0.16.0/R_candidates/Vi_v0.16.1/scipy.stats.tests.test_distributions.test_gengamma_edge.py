def test_gengamma_edge():
    # Regression test for gh-3985.
    p = stats.gengamma.pdf(0, 1, 1)
    assert_equal(p, 1.0)

    # Regression tests for gh-4724.
    p = stats.gengamma._munp(-2, 200, 1.)
    assert_almost_equal(p, 1./199/198)

    p = stats.gengamma._munp(-2, 10, 1.)
    assert_almost_equal(p, 1./9/8)
