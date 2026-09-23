def test_magic_square():
    A, b, c, numbers = magic_square(3)
    A1, b1, status, message = _remove_redundancy(A, b)
    assert_equal(status, 0)
    assert_equal(A1.shape[0], 23)
    assert_equal(np.linalg.matrix_rank(A1), 23)
