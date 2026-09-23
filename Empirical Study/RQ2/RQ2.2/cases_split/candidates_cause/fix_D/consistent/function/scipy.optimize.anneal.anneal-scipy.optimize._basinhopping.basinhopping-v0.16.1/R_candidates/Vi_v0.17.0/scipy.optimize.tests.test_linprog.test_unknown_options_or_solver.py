def test_unknown_options_or_solver():
    c = np.array([-3,-2])
    A_ub = [[2,1], [1,1], [1,0]]
    b_ub = [10,8,4]

    _assert_warns(OptimizeWarning, linprog,
                  c, A_ub=A_ub, b_ub=b_ub, options=dict(spam='42'))

    assert_raises(ValueError, linprog,
                  c, A_ub=A_ub, b_ub=b_ub, method='ekki-ekki-ekki')
