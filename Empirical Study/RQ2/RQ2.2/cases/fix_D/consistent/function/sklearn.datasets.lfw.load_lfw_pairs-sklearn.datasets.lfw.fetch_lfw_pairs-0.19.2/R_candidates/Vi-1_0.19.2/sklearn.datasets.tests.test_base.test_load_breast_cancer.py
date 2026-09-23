def test_load_breast_cancer():
    res = load_breast_cancer()
    assert_equal(res.data.shape, (569, 30))
    assert_equal(res.target.size, 569)
    assert_equal(res.target_names.size, 2)
    assert_true(res.DESCR)

    # test return_X_y option
    X_y_tuple = load_breast_cancer(return_X_y=True)
    bunch = load_breast_cancer()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
