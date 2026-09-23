def lstsq(a, b, cond=None, overwrite_a=False, overwrite_b=False,
          check_finite=True):
    """
    Compute least-squares solution to equation Ax = b.

    Compute a vector x such that the 2-norm ``|b - A x|`` is minimized.

    Parameters
    ----------
    a : (M, N) array_like
        Left hand side matrix (2-D array).
    b : (M,) or (M, K) array_like
        Right hand side matrix or vector (1-D or 2-D array).
    cond : float, optional
        Cutoff for 'small' singular values; used to determine effective
        rank of a. Singular values smaller than
        ``rcond * largest_singular_value`` are considered zero.
    overwrite_a : bool, optional
        Discard data in `a` (may enhance performance). Default is False.
    overwrite_b : bool, optional
        Discard data in `b` (may enhance performance). Default is False.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (N,) or (N, K) ndarray
        Least-squares solution.  Return shape matches shape of `b`.
    residues : () or (1,) or (K,) ndarray
        Sums of residues, squared 2-norm for each column in ``b - a x``.
        If rank of matrix a is < N or > M this is an empty array.
        If b was 1-D, this is an (1,) shape array, otherwise the shape is (K,).
    rank : int
        Effective rank of matrix `a`.
    s : (min(M,N),) ndarray
        Singular values of `a`. The condition number of a is
        ``abs(s[0]/s[-1])``.

    Raises
    ------
    LinAlgError :
        If computation does not converge.


    See Also
    --------
    optimize.nnls : linear least squares with non-negativity constraint

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    b1 = _asarray_validated(b, check_finite=check_finite)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    m, n = a1.shape
    if len(b1.shape) == 2:
        nrhs = b1.shape[1]
    else:
        nrhs = 1
    if m != b1.shape[0]:
        raise ValueError('incompatible dimensions')
    gelss, = get_lapack_funcs(('gelss',), (a1, b1))
    if n > m:
        # need to extend b matrix as it will be filled with
        # a larger solution matrix
        if len(b1.shape) == 2:
            b2 = np.zeros((n, nrhs), dtype=gelss.dtype)
            b2[:m,:] = b1
        else:
            b2 = np.zeros(n, dtype=gelss.dtype)
            b2[:m] = b1
        b1 = b2

    overwrite_a = overwrite_a or _datacopied(a1, a)
    overwrite_b = overwrite_b or _datacopied(b1, b)

    # get optimal work array
    work = gelss(a1, b1, lwork=-1)[4]
    lwork = work[0].real.astype(np.int)
    v, x, s, rank, work, info = gelss(
        a1, b1, cond=cond, lwork=lwork, overwrite_a=overwrite_a,
        overwrite_b=overwrite_b)

    if info > 0:
        raise LinAlgError("SVD did not converge in Linear Least Squares")
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gelss'
                                                                    % -info)
    resids = np.asarray([], dtype=x.dtype)
    if n < m:
        x1 = x[:n]
        if rank == n:
            resids = np.sum(np.abs(x[n:])**2, axis=0)
        x = x1
    return x, resids, rank, s
