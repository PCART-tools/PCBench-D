def test_aliasing_b_eq():
    c = np.array([1.0])
    A_eq = np.array([[1.0]])
    b_eq_orig = np.array([3.0])
    b_eq = b_eq_orig.copy()
    bounds = (-4.0, np.inf)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    _assert_success(res, desired_fun=3, desired_x=[3])
    assert_allclose(b_eq_orig, b_eq)
