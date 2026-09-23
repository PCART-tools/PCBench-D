def test_basic_artificial_vars():
    # Test if linprog succeeds when at the end of Phase 1 some artificial
    # variables remain basic, and the row in T corresponding to the
    # artificial variables is not all zero.
    c = np.array([-0.1, -0.07, 0.004, 0.004, 0.004, 0.004])
    A_ub = np.array([[1.0, 0, 0, 0, 0, 0], [-1.0, 0, 0, 0, 0, 0],
                     [0, -1.0, 0, 0, 0, 0], [0, 1.0, 0, 0, 0, 0],
                     [1.0, 1.0, 0, 0, 0, 0]])
    b_ub = np.array([3.0, 3.0, 3.0, 3.0, 20.0])
    A_eq = np.array([[1.0, 0, -1, 1, -1, 1], [0, -1.0, -1, 1, -1, 1]])
    b_eq = np.array([0, 0])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  callback=lambda x, **kwargs: None)
    _assert_success(res, desired_fun=0, desired_x=np.zeros_like(c))
