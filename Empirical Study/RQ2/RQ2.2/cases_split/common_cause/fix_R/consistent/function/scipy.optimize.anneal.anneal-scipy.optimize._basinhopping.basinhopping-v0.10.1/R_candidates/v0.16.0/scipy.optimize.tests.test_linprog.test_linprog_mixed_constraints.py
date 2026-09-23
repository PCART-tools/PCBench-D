def test_linprog_mixed_constraints():
    # Minimize linear function subject to non-negative variables.
    #  http://www.statslab.cam.ac.uk/~ff271/teaching/opt/notes/notes8.pdf
    c = [6,3]
    A_ub = [[0, 3],
           [-1,-1],
           [-2, 1]]
    b_ub = [2,-1,-1]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub)
    _assert_success(res, desired_fun=5, desired_x=[2/3, 1/3])
