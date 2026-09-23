def test_infeasible_m_eq_n():
    m, n = 10, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    A0[-1, :] = 2 * A0[-2, :]
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 2)
