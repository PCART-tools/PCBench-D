def test_infeasible_m_gt_n():
    m, n = 20, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 2)
