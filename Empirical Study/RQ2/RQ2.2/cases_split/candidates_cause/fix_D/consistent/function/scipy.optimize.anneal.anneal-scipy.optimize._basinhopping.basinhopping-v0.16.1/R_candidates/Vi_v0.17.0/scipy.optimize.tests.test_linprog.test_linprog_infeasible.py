def test_linprog_infeasible():
    # Test linrpog response to an infeasible problem
    c = [-1,-1]
    A_ub = [[1,0],
            [0,1],
            [-1,-1]]
    b_ub = [2,2,-5]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub)
    _assert_infeasible(res)
