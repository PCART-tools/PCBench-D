def test_load_svmlight_file():
    X, y = load_svmlight_file(datafile)

    # test X's shape
    assert_equal(X.indptr.shape[0], 7)
    assert_equal(X.shape[0], 6)
    assert_equal(X.shape[1], 21)
    assert_equal(y.shape[0], 6)

    # test X's non-zero values
    for i, j, val in ((0, 2, 2.5), (0, 10, -5.2), (0, 15, 1.5),
                     (1, 5, 1.0), (1, 12, -3),
                     (2, 20, 27)):

        assert_equal(X[i, j], val)

    # tests X's zero values
    assert_equal(X[0, 3], 0)
    assert_equal(X[0, 5], 0)
    assert_equal(X[1, 8], 0)
    assert_equal(X[1, 16], 0)
    assert_equal(X[2, 18], 0)

    # test can change X's values
    X[0, 2] *= 2
    assert_equal(X[0, 2], 5)

    # test y
    assert_array_equal(y, [1, 2, 3, 4, 1, 2])
