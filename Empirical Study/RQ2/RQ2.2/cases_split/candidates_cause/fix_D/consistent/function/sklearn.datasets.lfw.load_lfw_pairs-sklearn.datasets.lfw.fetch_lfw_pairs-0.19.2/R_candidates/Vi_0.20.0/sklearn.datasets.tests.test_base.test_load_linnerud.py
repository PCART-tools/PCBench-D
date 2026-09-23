def test_load_linnerud():
    res = load_linnerud()
    assert_equal(res.data.shape, (20, 3))
    assert_equal(res.target.shape, (20, 3))
    assert_equal(len(res.target_names), 3)
    assert_true(res.DESCR)
    assert_true(os.path.exists(res.data_filename))
    assert_true(os.path.exists(res.target_filename))

    # test return_X_y option
    check_return_X_y(res, partial(load_linnerud))
