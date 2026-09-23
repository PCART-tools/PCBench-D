def _sym_solve(Dinv, M, A, r1, r2, solve, splu=False):
    """
    An implementation of [1] equation 8.31 and 8.32

    References
    ----------
    .. [1] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.

    """
    # [1] 8.31
    r = r2 + A.dot(Dinv * r1)
    if splu:
        v = solve(r)
    else:
        v = solve(M, r)
    # [1] 8.32
    u = Dinv * (A.T.dot(v) - r1)
    return u, v
