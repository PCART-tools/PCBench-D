def test_empty():
    def fun(t, y):
        return np.zeros((0,))

    y0 = np.zeros((0,))

    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        sol = assert_no_warnings(solve_ivp, fun, [0, 10], y0,
                                 method=method, dense_output=True)
        assert_equal(sol.sol(10), np.zeros((0,)))
        assert_equal(sol.sol([1, 2, 3]), np.zeros((0, 3)))

    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        sol = assert_no_warnings(solve_ivp, fun, [0, np.inf], y0,
                                 method=method, dense_output=True)
        assert_equal(sol.sol(10), np.zeros((0,)))
        assert_equal(sol.sol([1, 2, 3]), np.zeros((0, 3)))
