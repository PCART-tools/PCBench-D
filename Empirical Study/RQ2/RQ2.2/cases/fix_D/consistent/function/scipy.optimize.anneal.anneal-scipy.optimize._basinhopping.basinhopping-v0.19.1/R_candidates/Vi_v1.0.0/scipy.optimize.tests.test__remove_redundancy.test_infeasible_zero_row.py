def test_infeasible_zero_row():
    A = np.eye(3)
    A[1, :] = 0
    b = np.random.rand(3)
    A1, b1, status, message = _remove_redundancy(A, b)
    assert_equal(status, 2)
