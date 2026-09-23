def test_load_diabetes():
    res = load_diabetes()
    assert_equal(res.data.shape, (442, 10))
    assert_true(res.target.size, 442)
    assert_equal(len(res.feature_names), 10)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_diabetes(return_X_y=True)
    bunch = load_diabetes()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
