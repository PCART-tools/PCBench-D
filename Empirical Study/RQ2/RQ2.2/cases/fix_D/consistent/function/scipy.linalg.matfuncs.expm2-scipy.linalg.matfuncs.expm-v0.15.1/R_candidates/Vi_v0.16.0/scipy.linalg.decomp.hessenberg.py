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
    check_finite : bool, optional
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
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or (a1.shape[0] != a1.shape[1]):
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))

    # if 2x2 or smaller: already in Hessenberg
    if a1.shape[0] <= 2:
        if calc_q:
            return a1, numpy.eye(a1.shape[0])
        return a1

    gehrd, gebal, gehrd_lwork = get_lapack_funcs(('gehrd','gebal', 'gehrd_lwork'), (a1,))
    ba, lo, hi, pivscale, info = gebal(a1, permute=0, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gebal '
                                                    '(hessenberg)' % -info)
    n = len(a1)

    lwork, info = gehrd_lwork(ba.shape[0], lo=lo, hi=hi)
    if info != 0:
        raise ValueError('failed to compute internal gehrd work array size. '
                            'LAPACK info = %d ' % info)
    lwork = int(lwork.real)

    hq, tau, info = gehrd(ba, lo=lo, hi=hi, lwork=lwork, overwrite_a=1)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gehrd '
                                        '(hessenberg)' % -info)
    h = numpy.triu(hq, -1)
    if not calc_q:
        return h

    # use orghr/unghr to compute q
    orghr, orghr_lwork = get_lapack_funcs(('orghr', 'orghr_lwork'), (a1,))
    lwork, info = orghr_lwork(n, lo=lo, hi=hi)
    if info != 0:
        raise ValueError('failed to compute internal orghr work array size. '
                            'LAPACK info = %d ' % info)
    lwork = int(lwork.real)
    q, info = orghr(a=hq, tau=tau, lo=lo, hi=hi, lwork=lwork, overwrite_a=1)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal orghr '
                         '(hessenberg)' % -info)
    return h, q
