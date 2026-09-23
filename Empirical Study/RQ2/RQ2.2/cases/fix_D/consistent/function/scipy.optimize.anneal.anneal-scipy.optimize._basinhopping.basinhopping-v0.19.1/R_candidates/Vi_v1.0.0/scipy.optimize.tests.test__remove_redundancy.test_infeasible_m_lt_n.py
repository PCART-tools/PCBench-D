def test_infeasible_m_lt_n():
    m, n = 9, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    A0[-1, :] = np.arange(m - 1).dot(A0[:-1])
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 2)
