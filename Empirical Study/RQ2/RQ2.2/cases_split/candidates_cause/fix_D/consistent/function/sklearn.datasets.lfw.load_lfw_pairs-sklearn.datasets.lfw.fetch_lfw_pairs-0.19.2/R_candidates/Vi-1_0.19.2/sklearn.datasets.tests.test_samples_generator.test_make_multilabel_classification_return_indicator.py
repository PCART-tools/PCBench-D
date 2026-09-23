def test_make_multilabel_classification_return_indicator():
    for allow_unlabeled, min_length in zip((True, False), (0, 1)):
        X, Y = make_multilabel_classification(n_samples=25, n_features=20,
                                              n_classes=3, random_state=0,
                                              allow_unlabeled=allow_unlabeled)
        assert_equal(X.shape, (25, 20), "X shape mismatch")
        assert_equal(Y.shape, (25, 3), "Y shape mismatch")
        assert_true(np.all(np.sum(Y, axis=0) > min_length))

    # Also test return_distributions and return_indicator with True
    X2, Y2, p_c, p_w_c = make_multilabel_classification(
        n_samples=25, n_features=20, n_classes=3, random_state=0,
        allow_unlabeled=allow_unlabeled, return_distributions=True)

    assert_array_equal(X, X2)
    assert_array_equal(Y, Y2)
    assert_equal(p_c.shape, (3,))
    assert_almost_equal(p_c.sum(), 1)
    assert_equal(p_w_c.shape, (20, 3))
    assert_almost_equal(p_w_c.sum(axis=0), [1] * 3)
