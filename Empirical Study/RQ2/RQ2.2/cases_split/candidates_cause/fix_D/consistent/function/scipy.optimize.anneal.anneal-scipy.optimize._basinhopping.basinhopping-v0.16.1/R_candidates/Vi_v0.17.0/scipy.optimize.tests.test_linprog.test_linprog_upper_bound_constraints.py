def test_linprog_upper_bound_constraints():
    # Maximize a linear function subject to only linear upper bound constraints.
    #  http://www.dam.brown.edu/people/huiwang/classes/am121/Archive/simplex_121_c.pdf
    c = np.array([3,2])*-1  # maximize
    A_ub = [[2,1],
            [1,1],
            [1,0]]
    b_ub = [10,8,4]
    res = (linprog(c,A_ub=A_ub,b_ub=b_ub))
    _assert_success(res, desired_fun=-18, desired_x=[2, 6])
