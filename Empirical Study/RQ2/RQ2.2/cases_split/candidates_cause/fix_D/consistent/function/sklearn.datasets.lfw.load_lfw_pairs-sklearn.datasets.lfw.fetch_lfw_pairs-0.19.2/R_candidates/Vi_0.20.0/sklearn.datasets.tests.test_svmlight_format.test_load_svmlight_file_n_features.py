def test_load_svmlight_file_n_features():
    X, y = load_svmlight_file(datafile, n_features=22)

    # test X'shape
    assert_equal(X.indptr.shape[0], 7)
    assert_equal(X.shape[0], 6)
    assert_equal(X.shape[1], 22)

    # test X's non-zero values
    for i, j, val in ((0, 2, 2.5), (0, 10, -5.2),
                     (1, 5, 1.0), (1, 12, -3)):

        assert_equal(X[i, j], val)

    # 21 features in file
    assert_raises(ValueError, load_svmlight_file, datafile, n_features=20)
