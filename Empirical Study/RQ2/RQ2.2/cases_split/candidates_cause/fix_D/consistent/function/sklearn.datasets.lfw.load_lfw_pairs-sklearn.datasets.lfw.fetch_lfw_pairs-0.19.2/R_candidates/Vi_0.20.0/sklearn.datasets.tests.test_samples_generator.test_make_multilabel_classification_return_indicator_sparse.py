def test_make_multilabel_classification_return_indicator_sparse():
    for allow_unlabeled, min_length in zip((True, False), (0, 1)):
        X, Y = make_multilabel_classification(n_samples=25, n_features=20,
                                              n_classes=3, random_state=0,
                                              return_indicator='sparse',
                                              allow_unlabeled=allow_unlabeled)
        assert_equal(X.shape, (25, 20), "X shape mismatch")
        assert_equal(Y.shape, (25, 3), "Y shape mismatch")
        assert_true(sp.issparse(Y))
