def test_make_spd_matrix():
    X = make_spd_matrix(n_dim=5, random_state=0)

    assert_equal(X.shape, (5, 5), "X shape mismatch")
    assert_array_almost_equal(X, X.T)

    from numpy.linalg import eig
    eigenvalues, _ = eig(X)
    assert_array_equal(eigenvalues > 0, np.array([True] * 5),
                       "X is not positive-definite")
