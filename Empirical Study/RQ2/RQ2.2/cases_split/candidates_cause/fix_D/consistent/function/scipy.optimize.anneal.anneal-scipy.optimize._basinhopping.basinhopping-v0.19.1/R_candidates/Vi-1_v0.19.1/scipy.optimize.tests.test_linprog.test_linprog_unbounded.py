def test_linprog_unbounded():
    # Test linprog response to an unbounded problem
    c = np.array([1,1])*-1  # maximize
    A_ub = [[-1,1],
            [-1,-1]]
    b_ub = [-1,-2]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub)
    _assert_unbounded(res)
