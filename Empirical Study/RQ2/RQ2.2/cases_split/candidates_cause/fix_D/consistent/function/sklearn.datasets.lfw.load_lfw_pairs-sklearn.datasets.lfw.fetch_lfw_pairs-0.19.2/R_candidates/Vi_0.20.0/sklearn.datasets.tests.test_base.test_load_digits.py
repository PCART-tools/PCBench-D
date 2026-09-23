def test_load_digits():
    digits = load_digits()
    assert_equal(digits.data.shape, (1797, 64))
    assert_equal(numpy.unique(digits.target).size, 10)

    # test return_X_y option
    check_return_X_y(digits, partial(load_digits))
