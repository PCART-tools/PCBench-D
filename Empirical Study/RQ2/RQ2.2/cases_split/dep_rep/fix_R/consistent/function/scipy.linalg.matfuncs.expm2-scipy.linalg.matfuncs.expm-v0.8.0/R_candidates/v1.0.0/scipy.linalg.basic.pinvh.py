def pinvh(a, cond=None, rcond=None, lower=True, return_rank=False,
          check_finite=True):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a Hermitian matrix.

    Calculate a generalized inverse of a Hermitian or real symmetric matrix
    using its eigenvalue decomposition and including all eigenvalues with
    'large' absolute value.

    Parameters
    ----------
    a : (N, N) array_like
        Real symmetric or complex hermetian matrix to be pseudo-inverted
    cond, rcond : float or None
        Cutoff for 'small' eigenvalues.
        Singular values smaller than rcond * largest_eigenvalue are considered
        zero.

        If None or -1, suitable machine precision is used.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of a. (Default: lower)
    return_rank : bool, optional
        if True, return the effective rank of the matrix
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    B : (N, N) ndarray
        The pseudo-inverse of matrix `a`.
    rank : int
        The effective rank of the matrix.  Returned if return_rank == True

    Raises
    ------
    LinAlgError
        If eigenvalue does not converge

    Examples
    --------
    >>> from scipy.linalg import pinvh
    >>> a = np.random.randn(9, 6)
    >>> a = np.dot(a, a.T)
    >>> B = pinvh(a)
    >>> np.allclose(a, np.dot(a, np.dot(B, a)))
    True
    >>> np.allclose(B, np.dot(B, np.dot(a, B)))
    True

    """
    a = _asarray_validated(a, check_finite=check_finite)
    s, u = decomp.eigh(a, lower=lower, check_finite=False)

    if rcond is not None:
        cond = rcond
    if cond in [None, -1]:
        t = u.dtype.char.lower()
        factor = {'f': 1E3, 'd': 1E6}
        cond = factor[t] * np.finfo(t).eps

    # For Hermitian matrices, singular values equal abs(eigenvalues)
    above_cutoff = (abs(s) > cond * np.max(abs(s)))
    psigma_diag = 1.0 / s[above_cutoff]
    u = u[:, above_cutoff]

    B = np.dot(u * psigma_diag, np.conjugate(u).T)

    if return_rank:
        return B, len(psigma_diag)
    else:
        return B
