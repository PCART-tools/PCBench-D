def test_load_iris():
    res = load_iris()
    assert_equal(res.data.shape, (150, 4))
    assert_equal(res.target.size, 150)
    assert_equal(res.target_names.size, 3)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_iris(return_X_y=True)
    bunch = load_iris()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
