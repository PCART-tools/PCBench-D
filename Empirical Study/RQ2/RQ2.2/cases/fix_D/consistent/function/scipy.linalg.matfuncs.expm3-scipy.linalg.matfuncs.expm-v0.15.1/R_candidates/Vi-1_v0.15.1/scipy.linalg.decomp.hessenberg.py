def hessenberg(a, calc_q=False, overwrite_a=False, check_finite=True):
    """
    Compute Hessenberg form of a matrix.

    The Hessenberg decomposition is::

        A = Q H Q^H

    where `Q` is unitary/orthogonal and `H` has only zero elements below
    the first sub-diagonal.

    Parameters
    ----------
    a : (M, M) array_like
        Matrix to bring into Hessenberg form.
    calc_q : bool, optional
        Whether to compute the transformation matrix.  Default is False.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.
        Default is False.
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    H : (M, M) ndarray
        Hessenberg form of `a`.
    Q : (M, M) ndarray
        Unitary/orthogonal similarity transformation matrix ``A = Q H Q^H``.
        Only returned if ``calc_q=True``.

    """
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if len(a1.shape) != 2 or (a1.shape[0] != a1.shape[1]):
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    gehrd, gebal, gehrd_lwork = get_lapack_funcs(('gehrd','gebal', 'gehrd_lwork'), (a1,))
    ba, lo, hi, pivscale, info = gebal(a1, permute=0, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gebal '
                                                    '(hessenberg)' % -info)
    n = len(a1)

    lwork, info = gehrd_lwork(ba.shape[0], lo=lo, hi=hi)
    if info != 0:
        raise ValueError('failed to compute internal gehrd work array size' % info)
    lwork = int(lwork.real)

    hq, tau, info = gehrd(ba, lo=lo, hi=hi, lwork=lwork, overwrite_a=1)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gehrd '
                                        '(hessenberg)' % -info)

    if not calc_q:
        for i in range(lo, hi):
            hq[i+2:hi+1, i] = 0.0
        return hq

    # XXX: Use ORGHR routines to compute q.
    typecode = hq.dtype
    ger,gemm = get_blas_funcs(('ger','gemm'), dtype=typecode)
    q = None
    for i in range(lo, hi):
        if tau[i] == 0.0:
            continue
        v = zeros(n, dtype=typecode)
        v[i+1] = 1.0
        v[i+2:hi+1] = hq[i+2:hi+1, i]
        hq[i+2:hi+1, i] = 0.0
        h = ger(-tau[i], v, v,a=diag(ones(n, dtype=typecode)), overwrite_a=1)
        if q is None:
            q = h
        else:
            q = gemm(1.0, q, h)
    if q is None:
        q = diag(ones(n, dtype=typecode))
    return hq, q
