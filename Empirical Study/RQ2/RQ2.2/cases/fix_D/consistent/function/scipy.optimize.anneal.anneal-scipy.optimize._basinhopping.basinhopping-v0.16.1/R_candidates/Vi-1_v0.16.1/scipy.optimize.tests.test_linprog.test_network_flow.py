def test_network_flow():
    # A network flow problem with supply and demand at nodes
    # and with costs along directed edges.
    # https://www.princeton.edu/~rvdb/542/lectures/lec10.pdf
    c = [2, 4, 9, 11, 4, 3, 8, 7, 0, 15, 16, 18]
    n, p = -1, 1
    A_eq = [
            [n, n, p, 0, p, 0, 0, 0, 0, p, 0, 0],
            [p, 0, 0, p, 0, p, 0, 0, 0, 0, 0, 0],
            [0, 0, n, n, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, p, p, 0, 0, p, 0],
            [0, 0, 0, 0, n, n, n, 0, p, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, n, n, 0, 0, p],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, n, n, n]]
    b_eq = [0, 19, -16, 33, 0, 0, -36]
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq)
    _assert_success(res, desired_fun=755)
