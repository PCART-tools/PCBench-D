def test_make_hastie_10_2():
    X, y = make_hastie_10_2(n_samples=100, random_state=0)
    assert_equal(X.shape, (100, 10), "X shape mismatch")
    assert_equal(y.shape, (100,), "y shape mismatch")
    assert_equal(np.unique(y).shape, (2,), "Unexpected number of classes")
