def test_network_flow_limited_capacity():
    # A network flow problem with supply and demand at nodes
    # and with costs and capacities along directed edges.
    # http://blog.sommer-forst.de/2013/04/10/
    cost = [2, 2, 1, 3, 1]
    bounds = [
            [0, 4],
            [0, 2],
            [0, 2],
            [0, 3],
            [0, 5]]
    n, p = -1, 1
    A_eq = [
            [n, n, 0, 0, 0],
            [p, 0, n, n, 0],
            [0, p, p, 0, n],
            [0, 0, 0, p, p]]
    b_eq = [-4, 0, 0, 4]
    # Including the callback here ensures the solution can be
    # calculated correctly, even when phase 1 terminated
    # with some of the artificial variables as pivots
    # (i.e. basis[:m] contains elements corresponding to
    # the artificial variables)
    res = linprog(c=cost, A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                  callback=lambda x, **kwargs: None)
    _assert_success(res, desired_fun=14)
