def test_aliasing():
    c = 1
    A_ub = [[1]]
    b_ub = [1]
    A_eq = [[1]]
    b_eq = [1]
    bounds = (-np.inf, np.inf)

    c_copy = deepcopy(c)
    A_ub_copy = deepcopy(A_ub)
    b_ub_copy = deepcopy(b_ub)
    A_eq_copy = deepcopy(A_eq)
    b_eq_copy = deepcopy(b_eq)
    bounds_copy = deepcopy(bounds)

    _clean_inputs(c, A_ub, b_ub, A_eq, b_eq, bounds)

    assert_(c == c_copy, "c modified by _clean_inputs")
    assert_(A_ub == A_ub_copy, "A_ub modified by _clean_inputs")
    assert_(b_ub == b_ub_copy, "b_ub modified by _clean_inputs")
    assert_(A_eq == A_eq_copy, "A_eq modified by _clean_inputs")
    assert_(b_eq == b_eq_copy, "b_eq modified by _clean_inputs")
    assert_(bounds == bounds_copy, "bounds modified by _clean_inputs")
