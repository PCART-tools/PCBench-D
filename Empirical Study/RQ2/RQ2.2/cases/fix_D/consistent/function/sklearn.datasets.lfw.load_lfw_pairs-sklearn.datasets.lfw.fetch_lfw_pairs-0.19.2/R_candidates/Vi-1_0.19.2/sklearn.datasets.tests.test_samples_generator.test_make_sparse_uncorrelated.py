def test_make_sparse_uncorrelated():
    X, y = make_sparse_uncorrelated(n_samples=5, n_features=10, random_state=0)

    assert_equal(X.shape, (5, 10), "X shape mismatch")
    assert_equal(y.shape, (5,), "y shape mismatch")
