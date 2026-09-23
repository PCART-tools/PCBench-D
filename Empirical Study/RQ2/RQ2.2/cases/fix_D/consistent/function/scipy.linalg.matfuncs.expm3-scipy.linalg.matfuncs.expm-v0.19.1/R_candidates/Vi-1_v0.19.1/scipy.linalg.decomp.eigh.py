def eigh(a, b=None, lower=True, eigvals_only=False, overwrite_a=False,
         overwrite_b=False, turbo=True, eigvals=None, type=1,
         check_finite=True):
    """
    Solve an ordinary or generalized eigenvalue problem for a complex
    Hermitian or real symmetric matrix.

    Find eigenvalues w and optionally eigenvectors v of matrix `a`, where
    `b` is positive definite::

                      a v[:,i] = w[i] b v[:,i]
        v[i,:].conj() a v[:,i] = w[i]
        v[i,:].conj() b v[:,i] = 1

    Parameters
    ----------
    a : (M, M) array_like
        A complex Hermitian or real symmetric matrix whose eigenvalues and
        eigenvectors will be computed.
    b : (M, M) array_like, optional
        A complex Hermitian or real symmetric definite positive matrix in.
        If omitted, identity matrix is assumed.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of `a`. (Default: lower)
    eigvals_only : bool, optional
        Whether to calculate only eigenvalues and no eigenvectors.
        (Default: both are calculated)
    turbo : bool, optional
        Use divide and conquer algorithm (faster but expensive in memory,
        only for generalized eigenvalue problem and if eigvals=None)
    eigvals : tuple (lo, hi), optional
        Indexes of the smallest and largest (in ascending order) eigenvalues
        and corresponding eigenvectors to be returned: 0 <= lo <= hi <= M-1.
        If omitted, all eigenvalues and eigenvectors are returned.
    type : int, optional
        Specifies the problem type to be solved:

           type = 1: a   v[:,i] = w[i] b v[:,i]

           type = 2: a b v[:,i] = w[i]   v[:,i]

           type = 3: b a v[:,i] = w[i]   v[:,i]
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance)
    overwrite_b : bool, optional
        Whether to overwrite data in `b` (may improve performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    w : (N,) float ndarray
        The N (1<=N<=M) selected eigenvalues, in ascending order, each
        repeated according to its multiplicity.
    v : (M, N) complex ndarray
        (if eigvals_only == False)

        The normalized selected eigenvector corresponding to the
        eigenvalue w[i] is the column v[:,i].

        Normalization:

            type 1 and 3: v.conj() a      v  = w

            type 2: inv(v).conj() a  inv(v) = w

            type = 1 or 2: v.conj() b      v  = I

            type = 3: v.conj() inv(b) v  = I

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge,
        an error occurred, or b matrix is not definite positive. Note that
        if input matrices are not symmetric or hermitian, no error is reported
        but results will be wrong.

    See Also
    --------
    eig : eigenvalues and right eigenvectors for non-symmetric arrays

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    if iscomplexobj(a1):
        cplx = True
    else:
        cplx = False
    if b is not None:
        b1 = _asarray_validated(b, check_finite=check_finite)
        overwrite_b = overwrite_b or _datacopied(b1, b)
        if len(b1.shape) != 2 or b1.shape[0] != b1.shape[1]:
            raise ValueError('expected square matrix')

        if b1.shape != a1.shape:
            raise ValueError("wrong b dimensions %s, should "
                             "be %s" % (str(b1.shape), str(a1.shape)))
        if iscomplexobj(b1):
            cplx = True
        else:
            cplx = cplx or False
    else:
        b1 = None

    # Set job for fortran routines
    _job = (eigvals_only and 'N') or 'V'

    # port eigenvalue range from python to fortran convention
    if eigvals is not None:
        lo, hi = eigvals
        if lo < 0 or hi >= a1.shape[0]:
            raise ValueError('The eigenvalue range specified is not valid.\n'
                             'Valid range is [%s,%s]' % (0, a1.shape[0]-1))
        lo += 1
        hi += 1
        eigvals = (lo, hi)

    # set lower
    if lower:
        uplo = 'L'
    else:
        uplo = 'U'

    # fix prefix for lapack routines
    if cplx:
        pfx = 'he'
    else:
        pfx = 'sy'

    #  Standard Eigenvalue Problem
    #  Use '*evr' routines
    # FIXME: implement calculation of optimal lwork
    #        for all lapack routines
    if b1 is None:
        (evr,) = get_lapack_funcs((pfx+'evr',), (a1,))
        if eigvals is None:
            w, v, info = evr(a1, uplo=uplo, jobz=_job, range="A", il=1,
                             iu=a1.shape[0], overwrite_a=overwrite_a)
        else:
            (lo, hi) = eigvals
            w_tot, v, info = evr(a1, uplo=uplo, jobz=_job, range="I",
                                 il=lo, iu=hi, overwrite_a=overwrite_a)
            w = w_tot[0:hi-lo+1]

    # Generalized Eigenvalue Problem
    else:
        # Use '*gvx' routines if range is specified
        if eigvals is not None:
            (gvx,) = get_lapack_funcs((pfx+'gvx',), (a1, b1))
            (lo, hi) = eigvals
            w_tot, v, ifail, info = gvx(a1, b1, uplo=uplo, iu=hi,
                                        itype=type, jobz=_job, il=lo,
                                        overwrite_a=overwrite_a,
                                        overwrite_b=overwrite_b)
            w = w_tot[0:hi-lo+1]
        # Use '*gvd' routine if turbo is on and no eigvals are specified
        elif turbo:
            (gvd,) = get_lapack_funcs((pfx+'gvd',), (a1, b1))
            v, w, info = gvd(a1, b1, uplo=uplo, itype=type, jobz=_job,
                             overwrite_a=overwrite_a,
                             overwrite_b=overwrite_b)
        # Use '*gv' routine if turbo is off and no eigvals are specified
        else:
            (gv,) = get_lapack_funcs((pfx+'gv',), (a1, b1))
            v, w, info = gv(a1, b1, uplo=uplo, itype=type, jobz=_job,
                            overwrite_a=overwrite_a,
                            overwrite_b=overwrite_b)

    # Check if we had a  successful exit
    if info == 0:
        if eigvals_only:
            return w
        else:
            return w, v

    elif info < 0:
        raise LinAlgError("illegal value in %i-th argument of internal"
                          " fortran routine." % (-info))
    elif info > 0 and b1 is None:
        raise LinAlgError("unrecoverable internal error.")

    # The algorithm failed to converge.
    elif 0 < info <= b1.shape[0]:
        if eigvals is not None:
            raise LinAlgError("the eigenvectors %s failed to"
                              " converge." % nonzero(ifail)-1)
        else:
            raise LinAlgError("internal fortran routine failed to converge: "
                              "%i off-diagonal elements of an "
                              "intermediate tridiagonal form did not converge"
                              " to zero." % info)

    # This occurs when b is not positive definite
    else:
        raise LinAlgError("the leading minor of order %i"
                          " of 'b' is not positive definite. The"
                          " factorization of 'b' could not be completed"
                          " and no eigenvalues or eigenvectors were"
                          " computed." % (info-b1.shape[0]))
