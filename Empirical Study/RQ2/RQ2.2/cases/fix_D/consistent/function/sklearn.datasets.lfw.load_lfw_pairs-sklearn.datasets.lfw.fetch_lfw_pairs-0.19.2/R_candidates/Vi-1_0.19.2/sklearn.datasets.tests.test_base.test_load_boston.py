def test_load_boston():
    res = load_boston()
    assert_equal(res.data.shape, (506, 13))
    assert_equal(res.target.size, 506)
    assert_equal(res.feature_names.size, 13)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_boston(return_X_y=True)
    bunch = load_boston()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
