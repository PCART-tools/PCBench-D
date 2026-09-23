def test_linprog_cyclic_recovery():
    # Test linprogs recovery from cycling using the Klee-Minty problem
    #  Klee-Minty  http://www.math.ubc.ca/~israel/m340/kleemin3.pdf
    c = np.array([100,10,1])*-1  # maximize
    A_ub = [[1, 0, 0],
            [20, 1, 0],
            [200,20, 1]]
    b_ub = [1,100,10000]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub)
    _assert_success(res, desired_x=[0, 0, 10000])
