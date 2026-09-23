def test_make_regression():
    X, y, c = make_regression(n_samples=100, n_features=10, n_informative=3,
                              effective_rank=5, coef=True, bias=0.0,
                              noise=1.0, random_state=0)

    assert_equal(X.shape, (100, 10), "X shape mismatch")
    assert_equal(y.shape, (100,), "y shape mismatch")
    assert_equal(c.shape, (10,), "coef shape mismatch")
    assert_equal(sum(c != 0.0), 3, "Unexpected number of informative features")

    # Test that y ~= np.dot(X, c) + bias + N(0, 1.0).
    assert_almost_equal(np.std(y - np.dot(X, c)), 1.0, decimal=1)

    # Test with small number of features.
    X, y = make_regression(n_samples=100, n_features=1)  # n_informative=3
    assert_equal(X.shape, (100, 1))
