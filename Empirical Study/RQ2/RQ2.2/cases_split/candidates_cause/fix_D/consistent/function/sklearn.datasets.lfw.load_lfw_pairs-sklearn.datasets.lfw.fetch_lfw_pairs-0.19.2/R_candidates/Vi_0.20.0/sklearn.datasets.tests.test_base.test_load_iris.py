def test_load_iris():
    res = load_iris()
    assert_equal(res.data.shape, (150, 4))
    assert_equal(res.target.size, 150)
    assert_equal(res.target_names.size, 3)
    assert_true(res.DESCR)
    assert_true(os.path.exists(res.filename))

    # test return_X_y option
    check_return_X_y(res, partial(load_iris))
