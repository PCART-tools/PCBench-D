def test_dense1():
    A = np.ones((6, 6))
    A[0, :3] = 0
    A[1, 3:] = 0
    A[3:, ::2] = -1
    A[3, :2] = 0
    A[4, 2:] = 0
    b = np.zeros(A.shape[0])

    A2 = A[[0, 1, 3, 4], :]
    b2 = np.zeros(4)

    A1, b1, status, message = _remove_redundancy(A, b)
    assert_allclose(A1, A2)
    assert_allclose(b1, b2)
    assert_equal(status, 0)
