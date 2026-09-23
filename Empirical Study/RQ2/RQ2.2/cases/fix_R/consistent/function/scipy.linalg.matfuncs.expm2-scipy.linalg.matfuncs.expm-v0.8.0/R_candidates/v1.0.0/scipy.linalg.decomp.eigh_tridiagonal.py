def eigh_tridiagonal(d, e, eigvals_only=False, select='a', select_range=None,
                     check_finite=True, tol=0., lapack_driver='auto'):
    """
    Solve eigenvalue problem for a real symmetric tridiagonal matrix.

    Find eigenvalues `w` and optionally right eigenvectors `v` of ``a``::

        a v[:,i] = w[i] v[:,i]
        v.H v    = identity

    For a real symmetric matrix ``a`` with diagonal elements `d` and
    off-diagonal elements `e`.

    Parameters
    ----------
    d : ndarray, shape (ndim,)
        The diagonal elements of the array.
    e : ndarray, shape (ndim-1,)
        The off-diagonal elements of the array.
    select : {'a', 'v', 'i'}, optional
        Which eigenvalues to calculate

        ======  ========================================
        select  calculated
        ======  ========================================
        'a'     All eigenvalues
        'v'     Eigenvalues in the interval (min, max]
        'i'     Eigenvalues with indices min <= i <= max
        ======  ========================================
    select_range : (min, max), optional
        Range of selected eigenvalues
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    tol : float
        The absolute tolerance to which each eigenvalue is required
        (only used when 'stebz' is the `lapack_driver`).
        An eigenvalue (or cluster) is considered to have converged if it
        lies in an interval of this width. If <= 0. (default),
        the value ``eps*|a|`` is used where eps is the machine precision,
        and ``|a|`` is the 1-norm of the matrix ``a``.
    lapack_driver : str
        LAPACK function to use, can be 'auto', 'stemr', 'stebz', 'sterf',
        or 'stev'. When 'auto' (default), it will use 'stemr' if ``select='a'``
        and 'stebz' otherwise. When 'stebz' is used to find the eigenvalues and
        ``eigvals_only=False``, then a second LAPACK call (to ``?STEIN``) is
        used to find the corresponding eigenvectors. 'sterf' can only be
        used when ``eigvals_only=True`` and ``select='a'``. 'stev' can only
        be used when ``select='a'``.

    Returns
    -------
    w : (M,) ndarray
        The eigenvalues, in ascending order, each repeated according to its
        multiplicity.
    v : (M, M) ndarray
        The normalized eigenvector corresponding to the eigenvalue ``w[i]`` is
        the column ``v[:,i]``.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge.

    See Also
    --------
    eigvalsh_tridiagonal : eigenvalues of symmetric/Hermitian tridiagonal
        matrices
    eig : eigenvalues and right eigenvectors for non-symmetric arrays
    eigh : eigenvalues and right eigenvectors for symmetric/Hermitian arrays
    eig_banded : eigenvalues and right eigenvectors for symmetric/Hermitian
        band matrices

    Notes
    -----
    This function makes use of LAPACK ``S/DSTEMR`` routines.
    """
    d = _asarray_validated(d, check_finite=check_finite)
    e = _asarray_validated(e, check_finite=check_finite)
    for check in (d, e):
        if check.ndim != 1:
            raise ValueError('expected one-dimensional array')
        if check.dtype.char in 'GFD':  # complex
            raise TypeError('Only real arrays currently supported')
    if d.size != e.size + 1:
        raise ValueError('d (%s) must have one more element than e (%s)'
                         % (d.size, e.size))
    select, vl, vu, il, iu, _ = _check_select(
        select, select_range, 0, d.size)
    if not isinstance(lapack_driver, string_types):
        raise TypeError('lapack_driver must be str')
    drivers = ('auto', 'stemr', 'sterf', 'stebz', 'stev')
    if lapack_driver not in drivers:
        raise ValueError('lapack_driver must be one of %s, got %s'
                         % (drivers, lapack_driver))
    if lapack_driver == 'auto':
        lapack_driver = 'stemr' if select == 0 else 'stebz'
    func, = get_lapack_funcs((lapack_driver,), (d, e))
    compute_v = not eigvals_only
    if lapack_driver == 'sterf':
        if select != 0:
            raise ValueError('sterf can only be used when select == "a"')
        if not eigvals_only:
            raise ValueError('sterf can only be used when eigvals_only is '
                             'True')
        w, info = func(d, e)
        m = len(w)
    elif lapack_driver == 'stev':
        if select != 0:
            raise ValueError('stev can only be used when select == "a"')
        w, v, info = func(d, e, compute_v=compute_v)
        m = len(w)
    elif lapack_driver == 'stebz':
        tol = float(tol)
        internal_name = 'stebz'
        stebz, = get_lapack_funcs((internal_name,), (d, e))
        # If getting eigenvectors, needs to be block-ordered (B) instead of
        # matirx-ordered (E), and we will reorder later
        order = 'E' if eigvals_only else 'B'
        m, w, iblock, isplit, info = stebz(d, e, select, vl, vu, il, iu, tol,
                                           order)
    else:   # 'stemr'
        # ?STEMR annoyingly requires size N instead of N-1
        e_ = empty(e.size+1, e.dtype)
        e_[:-1] = e
        stemr_lwork, = get_lapack_funcs(('stemr_lwork',), (d, e))
        lwork, liwork, info = stemr_lwork(d, e_, select, vl, vu, il, iu,
                                          compute_v=compute_v)
        _check_info(info, 'stemr_lwork')
        m, w, v, info = func(d, e_, select, vl, vu, il, iu,
                             compute_v=compute_v, lwork=lwork, liwork=liwork)
    _check_info(info, lapack_driver + ' (eigh_tridiagonal)')
    w = w[:m]
    if eigvals_only:
        return w
    else:
        # Do we still need to compute the eigenvalues?
        if lapack_driver == 'stebz':
            func, = get_lapack_funcs(('stein',), (d, e))
            v, info = func(d, e, w, iblock, isplit)
            _check_info(info, 'stein (eigh_tridiagonal)',
                        positive='%d eigenvectors failed to converge')
            # Convert block-order to matrix-order
            order = argsort(w)
            w, v = w[order], v[:, order]
        else:
            v = v[:, :m]
        return w, v
