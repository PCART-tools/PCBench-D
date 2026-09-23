def test_dense2():
    A = np.eye(6)
    A[-2, -1] = 1
    A[-1, :] = 1
    b = np.zeros(A.shape[0])
    A1, b1, status, message = _remove_redundancy(A, b)
    assert_allclose(A1, A[:-1, :])
    assert_allclose(b1, b[:-1])
    assert_equal(status, 0)
