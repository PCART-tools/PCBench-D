def eig(a, b=None, left=False, right=True, overwrite_a=False,
        overwrite_b=False, check_finite=True):
    """
    Solve an ordinary or generalized eigenvalue problem of a square matrix.

    Find eigenvalues w and right or left eigenvectors of a general matrix::

        a   vr[:,i] = w[i]        b   vr[:,i]
        a.H vl[:,i] = w[i].conj() b.H vl[:,i]

    where ``.H`` is the Hermitian conjugation.

    Parameters
    ----------
    a : (M, M) array_like
        A complex or real matrix whose eigenvalues and eigenvectors
        will be computed.
    b : (M, M) array_like, optional
        Right-hand side matrix in a generalized eigenvalue problem.
        Default is None, identity matrix is assumed.
    left : bool, optional
        Whether to calculate and return left eigenvectors.  Default is False.
    right : bool, optional
        Whether to calculate and return right eigenvectors.  Default is True.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.  Default is False.
    overwrite_b : bool, optional
        Whether to overwrite `b`; may improve performance.  Default is False.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    w : (M,) double or complex ndarray
        The eigenvalues, each repeated according to its multiplicity.
    vl : (M, M) double or complex ndarray
        The normalized left eigenvector corresponding to the eigenvalue
        ``w[i]`` is the column vl[:,i]. Only returned if ``left=True``.
    vr : (M, M) double or complex ndarray
        The normalized right eigenvector corresponding to the eigenvalue
        ``w[i]`` is the column ``vr[:,i]``.  Only returned if ``right=True``.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge.

    See Also
    --------
    eigh : Eigenvalues and right eigenvectors for symmetric/Hermitian arrays.

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    if b is not None:
        b1 = _asarray_validated(b, check_finite=check_finite)
        overwrite_b = overwrite_b or _datacopied(b1, b)
        if len(b1.shape) != 2 or b1.shape[0] != b1.shape[1]:
            raise ValueError('expected square matrix')
        if b1.shape != a1.shape:
            raise ValueError('a and b must have the same shape')
        return _geneig(a1, b1, left, right, overwrite_a, overwrite_b)

    geev, geev_lwork = get_lapack_funcs(('geev', 'geev_lwork'), (a1,))
    compute_vl, compute_vr = left, right

    lwork, info = geev_lwork(a1.shape[0],
                             compute_vl=compute_vl,
                             compute_vr=compute_vr)
    if info != 0:
        raise LinAlgError("internal *geev work array calculation failed: %d" % (info,))
    lwork = int(lwork.real)

    if geev.typecode in 'cz':
        w, vl, vr, info = geev(a1, lwork=lwork,
                               compute_vl=compute_vl,
                               compute_vr=compute_vr,
                               overwrite_a=overwrite_a)
    else:
        wr, wi, vl, vr, info = geev(a1, lwork=lwork,
                                    compute_vl=compute_vl,
                                    compute_vr=compute_vr,
                                    overwrite_a=overwrite_a)
        t = {'f':'F','d':'D'}[wr.dtype.char]
        w = wr + _I * wi

    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal geev'
                                                                    % -info)
    if info > 0:
        raise LinAlgError("eig algorithm did not converge (only eigenvalues "
                            "with order >= %d have converged)" % info)

    only_real = numpy.logical_and.reduce(numpy.equal(w.imag, 0.0))
    if not (geev.typecode in 'cz' or only_real):
        t = w.dtype.char
        if left:
            vl = _make_complex_eigvecs(w, vl, t)
        if right:
            vr = _make_complex_eigvecs(w, vr, t)
    if not (left or right):
        return w
    if left:
        if right:
            return w, vl, vr
        return w, vl
    return w, vr
