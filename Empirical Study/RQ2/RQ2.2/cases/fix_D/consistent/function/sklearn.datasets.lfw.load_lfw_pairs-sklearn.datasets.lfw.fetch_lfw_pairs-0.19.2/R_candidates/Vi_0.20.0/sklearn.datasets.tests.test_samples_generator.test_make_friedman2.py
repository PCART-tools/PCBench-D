def test_make_friedman2():
    X, y = make_friedman2(n_samples=5, noise=0.0, random_state=0)

    assert_equal(X.shape, (5, 4), "X shape mismatch")
    assert_equal(y.shape, (5,), "y shape mismatch")

    assert_array_almost_equal(y,
                              (X[:, 0] ** 2
                               + (X[:, 1] * X[:, 2] - 1
                                  / (X[:, 1] * X[:, 3])) ** 2) ** 0.5)
