def test_simple_values():
    alpha = np.array([1, 1])
    d = dirichlet(alpha)

    assert_almost_equal(d.mean(), 0.5)
    assert_almost_equal(d.var(), 1. / 12.)

    b = beta(1, 1)
    assert_almost_equal(d.mean(), b.mean())
    assert_almost_equal(d.var(), b.var())
