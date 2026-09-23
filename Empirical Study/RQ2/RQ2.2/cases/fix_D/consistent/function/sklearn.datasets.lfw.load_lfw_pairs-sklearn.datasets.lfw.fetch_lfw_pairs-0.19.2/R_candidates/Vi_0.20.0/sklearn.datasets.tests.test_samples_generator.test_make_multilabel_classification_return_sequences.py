def test_make_multilabel_classification_return_sequences():
    for allow_unlabeled, min_length in zip((True, False), (0, 1)):
        X, Y = make_multilabel_classification(n_samples=100, n_features=20,
                                              n_classes=3, random_state=0,
                                              return_indicator=False,
                                              allow_unlabeled=allow_unlabeled)
        assert_equal(X.shape, (100, 20), "X shape mismatch")
        if not allow_unlabeled:
            assert_equal(max([max(y) for y in Y]), 2)
        assert_equal(min([len(y) for y in Y]), min_length)
        assert_true(max([len(y) for y in Y]) <= 3)
