def _check_orth(n):
    X = np.ones((n, 2), dtype=float)
    Y = orth(X)
    assert_equal(Y.shape, (n, 1))
    assert_allclose(Y, Y.mean(), atol=1e-10)
    Y = orth(X.T)
    assert_equal(Y.shape, (2, 1))
    assert_allclose(Y, Y.mean())
