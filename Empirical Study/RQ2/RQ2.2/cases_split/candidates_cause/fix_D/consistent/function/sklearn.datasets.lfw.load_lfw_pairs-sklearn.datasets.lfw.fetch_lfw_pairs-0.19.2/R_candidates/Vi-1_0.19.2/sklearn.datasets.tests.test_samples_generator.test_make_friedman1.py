def test_make_friedman1():
    X, y = make_friedman1(n_samples=5, n_features=10, noise=0.0,
                          random_state=0)

    assert_equal(X.shape, (5, 10), "X shape mismatch")
    assert_equal(y.shape, (5,), "y shape mismatch")

    assert_array_almost_equal(y,
                              10 * np.sin(np.pi * X[:, 0] * X[:, 1])
                              + 20 * (X[:, 2] - 0.5) ** 2
                              + 10 * X[:, 3] + 5 * X[:, 4])
