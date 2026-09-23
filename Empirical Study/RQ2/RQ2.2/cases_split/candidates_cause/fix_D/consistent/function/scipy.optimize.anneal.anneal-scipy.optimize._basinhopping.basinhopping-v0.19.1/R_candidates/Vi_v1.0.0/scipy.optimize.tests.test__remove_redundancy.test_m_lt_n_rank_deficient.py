def test_m_lt_n_rank_deficient():
    m, n = 9, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    A0[-1, :] = np.arange(m - 1).dot(A0[:-1])
    b0[-1] = np.arange(m - 1).dot(b0[:-1])
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 0)
    assert_equal(A1.shape[0], 8)
    assert_equal(np.linalg.matrix_rank(A1), 8)
