def test_enzo_example_b():
    # rescued from https://github.com/scipy/scipy/pull/218
    c = [2.8, 6.3, 10.8, -2.8, -6.3, -10.8]
    A_eq = [[-1, -1, -1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1]]
    b_eq = [-0.5, 0.4, 0.3, 0.3, 0.3]
    # Including the callback here ensures the solution can be
    # calculated correctly.
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq,
                  callback=lambda x, **kwargs: None)
    _assert_success(res, desired_fun=-1.77,
                    desired_x=[0.3, 0.2, 0.0, 0.0, 0.1, 0.3])
