def test_load_linnerud():
    res = load_linnerud()
    assert_equal(res.data.shape, (20, 3))
    assert_equal(res.target.shape, (20, 3))
    assert_equal(len(res.target_names), 3)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_linnerud(return_X_y=True)
    bunch = load_linnerud()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
