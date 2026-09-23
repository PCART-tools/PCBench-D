def svd(a, full_matrices=True, compute_uv=True, overwrite_a=False,
        check_finite=True):
    """
    Singular Value Decomposition.

    Factorizes the matrix a into two unitary matrices U and Vh, and
    a 1-D array s of singular values (real, non-negative) such that
    ``a == U*S*Vh``, where S is a suitably shaped matrix of zeros with
    main diagonal s.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to decompose.
    full_matrices : bool, optional
        If True, `U` and `Vh` are of shape ``(M,M)``, ``(N,N)``.
        If False, the shapes are ``(M,K)`` and ``(K,N)``, where
        ``K = min(M,N)``.
    compute_uv : bool, optional
        Whether to compute also `U` and `Vh` in addition to `s`.
        Default is True.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.
        Default is False.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    U : ndarray
        Unitary matrix having left singular vectors as columns.
        Of shape ``(M,M)`` or ``(M,K)``, depending on `full_matrices`.
    s : ndarray
        The singular values, sorted in non-increasing order.
        Of shape (K,), with ``K = min(M, N)``.
    Vh : ndarray
        Unitary matrix having right singular vectors as rows.
        Of shape ``(N,N)`` or ``(K,N)`` depending on `full_matrices`.

    For ``compute_uv = False``, only `s` is returned.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See also
    --------
    svdvals : Compute singular values of a matrix.
    diagsvd : Construct the Sigma matrix, given the vector s.

    Examples
    --------
    >>> from scipy import linalg
    >>> a = np.random.randn(9, 6) + 1.j*np.random.randn(9, 6)
    >>> U, s, Vh = linalg.svd(a)
    >>> U.shape, Vh.shape, s.shape
    ((9, 9), (6, 6), (6,))

    >>> U, s, Vh = linalg.svd(a, full_matrices=False)
    >>> U.shape, Vh.shape, s.shape
    ((9, 6), (6, 6), (6,))
    >>> S = linalg.diagsvd(s, 6, 6)
    >>> np.allclose(a, np.dot(U, np.dot(S, Vh)))
    True

    >>> s2 = linalg.svd(a, compute_uv=False)
    >>> np.allclose(s, s2)
    True

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    m,n = a1.shape
    overwrite_a = overwrite_a or (_datacopied(a1, a))

    gesdd, gesdd_lwork = get_lapack_funcs(('gesdd', 'gesdd_lwork'), (a1,))

    # compute optimal lwork
    lwork, info = gesdd_lwork(a1.shape[0], a1.shape[1], compute_uv=compute_uv, full_matrices=full_matrices)
    if info != 0:
        raise ValueError('work array size computation for internal gesdd failed: %d' % info)
    lwork = int(lwork.real)

    # perform decomposition
    u,s,v,info = gesdd(a1, compute_uv=compute_uv, lwork=lwork,
                       full_matrices=full_matrices, overwrite_a=overwrite_a)

    if info > 0:
        raise LinAlgError("SVD did not converge")
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gesdd'
                                                                    % -info)
    if compute_uv:
        return u, s, v
    else:
        return s
