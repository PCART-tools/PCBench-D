def test_gengamma_edge():
    # Regression test for gh-3985.
    p = stats.gengamma.pdf(0, 1, 1)
    assert_equal(p, 1.0)
