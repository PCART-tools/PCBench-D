def test_aliasing_b_ub():
    c = np.array([1.0])
    A_ub = np.array([[1.0]])
    b_ub_orig = np.array([3.0])
    b_ub = b_ub_orig.copy()
    bounds = (-4.0, np.inf)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
    _assert_success(res, desired_fun=-4, desired_x=[-4])
    assert_allclose(b_ub_orig, b_ub)
