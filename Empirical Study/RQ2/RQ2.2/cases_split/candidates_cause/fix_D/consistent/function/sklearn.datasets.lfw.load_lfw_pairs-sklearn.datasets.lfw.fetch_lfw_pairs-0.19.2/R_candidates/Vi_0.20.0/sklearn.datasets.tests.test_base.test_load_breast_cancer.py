def test_load_breast_cancer():
    res = load_breast_cancer()
    assert_equal(res.data.shape, (569, 30))
    assert_equal(res.target.size, 569)
    assert_equal(res.target_names.size, 2)
    assert_true(res.DESCR)
    assert_true(os.path.exists(res.filename))

    # test return_X_y option
    check_return_X_y(res, partial(load_breast_cancer))
