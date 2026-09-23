def test_no_redundancy():
    m, n = 10, 10
    A0 = np.random.rand(m, n)
    b0 = np.random.rand(m)
    A1, b1, status, message = _remove_redundancy(A0, b0)
    assert_allclose(A0, A1)
    assert_allclose(b0, b1)
    assert_equal(status, 0)
