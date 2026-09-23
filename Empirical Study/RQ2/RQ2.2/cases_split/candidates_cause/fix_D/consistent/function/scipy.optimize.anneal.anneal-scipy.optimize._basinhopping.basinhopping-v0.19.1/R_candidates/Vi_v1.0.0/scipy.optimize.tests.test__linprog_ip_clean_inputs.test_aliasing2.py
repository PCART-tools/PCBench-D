def test_aliasing2():
    c = np.array([1, 1])
    A_ub = np.array([[1, 1], [2, 2]])
    b_ub = np.array([[1], [1]])
    A_eq = np.array([[1, 1]])
    b_eq = np.array([1])
    bounds = [(-np.inf, np.inf), (None, 1)]

    c_copy = c.copy()
    A_ub_copy = A_ub.copy()
    b_ub_copy = b_ub.copy()
    A_eq_copy = A_eq.copy()
    b_eq_copy = b_eq.copy()
    bounds_copy = deepcopy(bounds)

    _clean_inputs(c, A_ub, b_ub, A_eq, b_eq, bounds)

    assert_allclose(c, c_copy, err_msg="c modified by _clean_inputs")
    assert_allclose(A_ub, A_ub_copy, err_msg="A_ub modified by _clean_inputs")
    assert_allclose(b_ub, b_ub_copy, err_msg="b_ub modified by _clean_inputs")
    assert_allclose(A_eq, A_eq_copy, err_msg="A_eq modified by _clean_inputs")
    assert_allclose(b_eq, b_eq_copy, err_msg="b_eq modified by _clean_inputs")
    assert_(bounds == bounds_copy, "bounds modified by _clean_inputs")
