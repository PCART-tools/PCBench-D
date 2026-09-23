def test_make_friedman3():
    X, y = make_friedman3(n_samples=5, noise=0.0, random_state=0)

    assert_equal(X.shape, (5, 4), "X shape mismatch")
    assert_equal(y.shape, (5,), "y shape mismatch")

    assert_array_almost_equal(y, np.arctan((X[:, 1] * X[:, 2]
                                            - 1 / (X[:, 1] * X[:, 3]))
                                           / X[:, 0]))
