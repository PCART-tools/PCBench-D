def test_m_gt_n_rank_deficient():
    m, n = 20, 10
    A0 = np.zeros((m, n))
    A0[:, 0] = 1
    b0 = np.ones(m)
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_equal(status, 0)
    assert_allclose(A1, A0[0:1, :])
    assert_allclose(b1, b0[0])
