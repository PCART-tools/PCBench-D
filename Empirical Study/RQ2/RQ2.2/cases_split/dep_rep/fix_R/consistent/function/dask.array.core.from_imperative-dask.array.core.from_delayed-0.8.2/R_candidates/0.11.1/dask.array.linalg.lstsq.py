def lstsq(a, b):
    """
    Return the least-squares solution to a linear matrix equation using
    QR decomposition.

    Solves the equation `a x = b` by computing a vector `x` that
    minimizes the Euclidean 2-norm `|| b - a x ||^2`.  The equation may
    be under-, well-, or over- determined (i.e., the number of
    linearly independent rows of `a` can be less than, equal to, or
    greater than its number of linearly independent columns).  If `a`
    is square and of full rank, then `x` (but for round-off error) is
    the "exact" solution of the equation.

    Parameters
    ----------
    a : (M, N) array_like
        "Coefficient" matrix.
    b : (M,) array_like
        Ordinate or "dependent variable" values.

    Returns
    -------
    x : (N,) Array
        Least-squares solution. If `b` is two-dimensional,
        the solutions are in the `K` columns of `x`.
    residuals : (1,) Array
        Sums of residuals; squared Euclidean 2-norm for each column in
        ``b - a*x``.
    rank : Array
        Rank of matrix `a`.
    s : (min(M, N),) Array
        Singular values of `a`.
    """
    q, r = qr(a)
    x = solve_triangular(r, q.T.dot(b))
    residuals = b - a.dot(x)
    residuals = (residuals ** 2).sum(keepdims=True)

    token = tokenize(a, b)

    # r must be a triangular with single block

    # rank
    rname = 'lstsq-rank-' + token
    rdsk = {(rname, ): (np.linalg.matrix_rank, (r.name, 0, 0))}
    rdsk.update(r.dask)
    # rank must be an integer
    rank = Array(rdsk, rname, shape=(), chunks=(), dtype=int)

    # singular
    sname = 'lstsq-singular-' + token
    rt = r.T
    sdsk = {(sname, 0): (_sort_decreasing,
                         (np.sqrt,
                          (np.linalg.eigvals,
                           (np.dot, (rt.name, 0, 0), (r.name, 0, 0)))))}
    sdsk.update(rt.dask)
    _, _, _, ss = np.linalg.lstsq(np.array([[1, 0], [1, 2]], dtype=a.dtype),
                           np.array([0, 1], dtype=b.dtype))
    s = Array(sdsk, sname, shape=(r.shape[0], ),
              chunks=r.shape[0], dtype=ss.dtype)

    return x, residuals, rank, s
