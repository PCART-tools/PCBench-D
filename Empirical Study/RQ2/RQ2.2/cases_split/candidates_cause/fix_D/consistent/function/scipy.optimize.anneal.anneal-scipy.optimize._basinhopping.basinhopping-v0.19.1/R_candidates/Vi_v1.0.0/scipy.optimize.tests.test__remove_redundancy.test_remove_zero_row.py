def test_remove_zero_row():
    A = np.eye(3)
    A[1, :] = 0
    b = np.random.rand(3)
    b[1] = 0
    A1, b1, status, message = _remove_redundancy(A, b)
    assert_equal(status, 0)
    assert_allclose(A1, A[[0, 2], :])
    assert_allclose(b1, b[[0, 2]])
