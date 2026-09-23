def test_negative_variable():
    # Test linprog with a problem with one unbounded variable and
    # another with a negative lower bound.
    c = np.array([-1,4])*-1  # maximize
    A_ub = np.array([[-3,1],
                     [1, 2]], dtype=np.float64)
    A_ub_orig = A_ub.copy()
    b_ub = [6,4]
    x0_bounds = (-np.inf,np.inf)
    x1_bounds = (-3,np.inf)

    res = linprog(c,A_ub=A_ub,b_ub=b_ub,bounds=(x0_bounds,x1_bounds))

    assert_equal(A_ub, A_ub_orig)   # user input not overwritten
    _assert_success(res, desired_fun=-80/7, desired_x=[-8/7, 18/7])
