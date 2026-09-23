def test_load_boston():
    res = load_boston()
    assert_equal(res.data.shape, (506, 13))
    assert_equal(res.target.size, 506)
    assert_equal(res.feature_names.size, 13)
    assert_true(res.DESCR)
    assert_true(os.path.exists(res.filename))

    # test return_X_y option
    check_return_X_y(res, partial(load_boston))
