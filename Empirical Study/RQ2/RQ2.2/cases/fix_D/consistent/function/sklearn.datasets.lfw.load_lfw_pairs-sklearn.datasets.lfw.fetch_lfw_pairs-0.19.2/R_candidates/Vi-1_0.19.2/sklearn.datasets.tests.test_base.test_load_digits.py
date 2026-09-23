def test_load_digits():
    digits = load_digits()
    assert_equal(digits.data.shape, (1797, 64))
    assert_equal(numpy.unique(digits.target).size, 10)

    # test return_X_y option
    X_y_tuple = load_digits(return_X_y=True)
    bunch = load_digits()
    assert_true(isinstance(X_y_tuple, tuple))
    assert_array_equal(X_y_tuple[0], bunch.data)
    assert_array_equal(X_y_tuple[1], bunch.target)
