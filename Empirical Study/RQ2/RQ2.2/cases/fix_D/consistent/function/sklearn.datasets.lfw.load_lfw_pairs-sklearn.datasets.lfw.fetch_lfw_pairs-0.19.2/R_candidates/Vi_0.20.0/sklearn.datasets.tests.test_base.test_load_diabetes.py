def test_load_diabetes():
    res = load_diabetes()
    assert_equal(res.data.shape, (442, 10))
    assert_true(res.target.size, 442)
    assert_equal(len(res.feature_names), 10)
    assert_true(res.DESCR)

    # test return_X_y option
    check_return_X_y(res, partial(load_diabetes))
