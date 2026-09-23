def test_load_wine():
    res = load_wine()
    assert_equal(res.data.shape, (178, 13))
    assert_equal(res.target.size, 178)
    assert_equal(res.target_names.size, 3)
    assert_true(res.DESCR)

    # test return_X_y option
    check_return_X_y(res, partial(load_wine))
