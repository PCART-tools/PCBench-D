def pinv2(a, cond=None, rcond=None, return_rank=False, check_finite=True):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.

    Calculate a generalized inverse of a matrix using its
    singular-value decomposition and including all 'large' singular
    values.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to be pseudo-inverted.
    cond, rcond : float or None
        Cutoff for 'small' singular values.
        Singular values smaller than ``rcond*largest_singular_value``
        are considered zero.
        If None or -1, suitable machine precision is used.
    return_rank : bool, optional
        if True, return the effective rank of the matrix
    check_finite : bool, optional
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
        If SVD computation does not converge.

    Examples
    --------
    >>> from scipy import linalg
    >>> a = np.random.randn(9, 6)
    >>> B = linalg.pinv2(a)
    >>> np.allclose(a, np.dot(a, np.dot(B, a)))
    True
    >>> np.allclose(B, np.dot(B, np.dot(a, B)))
    True

    """
    a = _asarray_validated(a, check_finite=check_finite)
    u, s, vh = decomp_svd.svd(a, full_matrices=False, check_finite=False)

    if rcond is not None:
        cond = rcond
    if cond in [None,-1]:
        t = u.dtype.char.lower()
        factor = {'f': 1E3, 'd': 1E6}
        cond = factor[t] * np.finfo(t).eps

    rank = np.sum(s > cond * np.max(s))
    psigma_diag = 1.0 / s[: rank]

    B = np.transpose(np.conjugate(np.dot(u[:, : rank] *
                                         psigma_diag, vh[: rank])))

    if return_rank:
        return B, rank
    else:
        return B
