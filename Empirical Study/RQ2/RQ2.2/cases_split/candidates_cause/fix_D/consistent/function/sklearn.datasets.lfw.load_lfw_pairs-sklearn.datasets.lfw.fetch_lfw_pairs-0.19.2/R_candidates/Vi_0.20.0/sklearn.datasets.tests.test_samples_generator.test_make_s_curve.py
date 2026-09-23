def test_make_s_curve():
    X, t = make_s_curve(n_samples=5, noise=0.0, random_state=0)

    assert_equal(X.shape, (5, 3), "X shape mismatch")
    assert_equal(t.shape, (5,), "t shape mismatch")
    assert_array_almost_equal(X[:, 0], np.sin(t))
    assert_array_almost_equal(X[:, 2], np.sign(t) * (np.cos(t) - 1))
