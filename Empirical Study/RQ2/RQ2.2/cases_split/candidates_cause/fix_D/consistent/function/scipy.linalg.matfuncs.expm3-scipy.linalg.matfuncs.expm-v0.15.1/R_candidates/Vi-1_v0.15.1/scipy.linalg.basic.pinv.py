def pinv(a, cond=None, rcond=None, return_rank=False, check_finite=True):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.

    Calculate a generalized inverse of a matrix using a least-squares
    solver.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to be pseudo-inverted.
    cond, rcond : float, optional
        Cutoff for 'small' singular values in the least-squares solver.
        Singular values smaller than ``rcond * largest_singular_value``
        are considered zero.
    return_rank : bool, optional
        if True, return the effective rank of the matrix
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    B : (N, M) ndarray
        The pseudo-inverse of matrix `a`.
    rank : int
        The effective rank of the matrix.  Returned if return_rank == True

    Raises
    ------
    LinAlgError
        If computation does not converge.

    Examples
    --------
    >>> a = np.random.randn(9, 6)
    >>> B = linalg.pinv(a)
    >>> np.allclose(a, dot(a, dot(B, a)))
    True
    >>> np.allclose(B, dot(B, dot(a, B)))
    True

    """
    if check_finite:
        a = np.asarray_chkfinite(a)
    else:
        a = np.asarray(a)
    b = np.identity(a.shape[0], dtype=a.dtype)
    if rcond is not None:
        cond = rcond

    x, resids, rank, s = lstsq(a, b, cond=cond, check_finite=False)

    if return_rank:
        return x, rank
    else:
        return x
