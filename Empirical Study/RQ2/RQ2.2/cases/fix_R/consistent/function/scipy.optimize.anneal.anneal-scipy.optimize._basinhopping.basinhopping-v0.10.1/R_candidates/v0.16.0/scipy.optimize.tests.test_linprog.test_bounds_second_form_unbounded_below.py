def test_bounds_second_form_unbounded_below():
    c = np.array([1.0])
    A_eq = np.array([[1.0]])
    b_eq = np.array([3.0])
    bounds = (None, 10.0)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    _assert_success(res, desired_fun=3, desired_x=[3])
