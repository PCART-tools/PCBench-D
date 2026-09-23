def test_invalid_inputs():
    for bad_bound in [[(5, 0), (1, 2), (3, 4)],
                      [(1, 2), (3, 4)],
                      [(1, 2), (3, 4), (3, 4, 5)],
                      [(1, 2), (np.inf, np.inf), (3, 4)],
                      [(1, 2), (-np.inf, -np.inf), (3, 4)],
                      ]:
        assert_raises(ValueError, linprog, [1, 2, 3], bounds=bad_bound)

    assert_raises(ValueError, linprog, [1,2], A_ub=[[1,2]], b_ub=[1,2])
    assert_raises(ValueError, linprog, [1,2], A_ub=[[1]], b_ub=[1])
    assert_raises(ValueError, linprog, [1,2], A_eq=[[1,2]], b_eq=[1,2])
    assert_raises(ValueError, linprog, [1,2], A_eq=[[1]], b_eq=[1])
    assert_raises(ValueError, linprog, [1,2], A_eq=[1], b_eq=1)
    assert_raises(ValueError, linprog, [1,2], A_ub=np.zeros((1,1,3)), b_eq=1)
