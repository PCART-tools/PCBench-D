def test_load_wine():
    res = load_wine()
    assert_equal(res.data.shape, (178, 13))
    assert_equal(res.target.size, 178)
    assert_equal(res.target_names.size, 3)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_wine(return_X_y=True)
    bunch = load_wine()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
