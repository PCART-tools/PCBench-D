def test_nontrivial_problem():
    # Test linprog for a problem involving all constraint types,
    # negative resource limits, and rounding issues.
    c = [-1,8,4,-6]
    A_ub = [[-7,-7,6,9],
            [1,-1,-3,0],
            [10,-10,-7,7],
            [6,-1,3,4]]
    b_ub = [-3,6,-6,6]
    A_eq = [[-10,1,1,-8]]
    b_eq = [-4]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq)
    _assert_success(res, desired_fun=7083/1391,
                    desired_x=[101/1391,1462/1391,0,752/1391])
