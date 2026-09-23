def test_m_gt_n():
    m, n = 20, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    x = np.linalg.solve(A0[:n, :], b0[:n])
    b0[n:] = A0[n:, :].dot(x)
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 0)
    assert_equal(A1.shape[0], n)
    assert_equal(np.linalg.matrix_rank(A1), n)
