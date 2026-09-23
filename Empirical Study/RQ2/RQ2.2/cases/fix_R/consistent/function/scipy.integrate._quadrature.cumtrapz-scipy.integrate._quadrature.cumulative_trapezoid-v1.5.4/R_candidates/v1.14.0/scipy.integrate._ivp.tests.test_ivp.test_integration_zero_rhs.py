@pytest.mark.parametrize('method', ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA'])
def test_integration_zero_rhs(method):
    result = solve_ivp(fun_zero, [0, 10], np.ones(3), method=method)
    assert_(result.success)
    assert_equal(result.status, 0)
    assert_allclose(result.y, 1.0, rtol=1e-15)
