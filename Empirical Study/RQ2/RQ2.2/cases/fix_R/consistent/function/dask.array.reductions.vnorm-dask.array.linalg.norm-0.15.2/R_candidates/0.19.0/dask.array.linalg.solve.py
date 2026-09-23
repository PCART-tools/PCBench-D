def solve(a, b, sym_pos=False):
    """
    Solve the equation ``a x = b`` for ``x``. By default, use LU
    decomposition and forward / backward substitutions. When ``sym_pos`` is
    ``True``, use Cholesky decomposition.

    Parameters
    ----------
    a : (M, M) array_like
        A square matrix.
    b : (M,) or (M, N) array_like
        Right-hand side matrix in ``a x = b``.
    sym_pos : bool
        Assume a is symmetric and positive definite. If ``True``, use Cholesky
        decomposition.

    Returns
    -------
    x : (M,) or (M, N) Array
        Solution to the system ``a x = b``.  Shape of the return matches the
        shape of `b`.
    """
    if sym_pos:
        l, u = _cholesky(a)
    else:
        p, l, u = lu(a)
        b = p.T.dot(b)
    uy = solve_triangular(l, b, lower=True)
    return solve_triangular(u, uy)
