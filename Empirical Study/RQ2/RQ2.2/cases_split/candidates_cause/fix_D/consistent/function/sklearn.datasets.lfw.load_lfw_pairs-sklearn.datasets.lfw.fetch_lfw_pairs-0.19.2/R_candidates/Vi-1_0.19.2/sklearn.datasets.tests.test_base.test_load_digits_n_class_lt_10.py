def test_load_digits_n_class_lt_10():
    digits = load_digits(9)
    assert_equal(digits.data.shape, (1617, 64))
    assert_equal(numpy.unique(digits.target).size, 9)
