def test_non_ndarray_args():
    c = [1.0]
    A_ub = [[1.0]]
    b_ub = [3.0]
    A_eq = [[1.0]]
    b_eq = [2.0]
    bounds = (-1.0, 10.0)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    _assert_success(res, desired_fun=2, desired_x=[2])
