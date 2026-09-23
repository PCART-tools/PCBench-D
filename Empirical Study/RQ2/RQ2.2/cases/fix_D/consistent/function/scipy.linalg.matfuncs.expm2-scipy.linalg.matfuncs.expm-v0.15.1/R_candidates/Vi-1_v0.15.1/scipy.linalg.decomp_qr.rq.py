def rq(a, overwrite_a=False, lwork=None, mode='full', check_finite=True):
    """
    Compute RQ decomposition of a matrix.

    Calculate the decomposition ``A = R Q`` where Q is unitary/orthogonal
    and R upper triangular.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to be decomposed
    overwrite_a : bool, optional
        Whether data in a is overwritten (may improve performance)
    lwork : int, optional
        Work array size, lwork >= a.shape[1]. If None or -1, an optimal size
        is computed.
    mode : {'full', 'r', 'economic'}, optional
        Determines what information is to be returned: either both Q and R
        ('full', default), only R ('r') or both Q and R but computed in
        economy-size ('economic', see Notes).
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    R : float or complex ndarray
        Of shape (M, N) or (M, K) for ``mode='economic'``.  ``K = min(M, N)``.
    Q : float or complex ndarray
        Of shape (N, N) or (K, N) for ``mode='economic'``.  Not returned
        if ``mode='r'``.

    Raises
    ------
    LinAlgError
        If decomposition fails.

    Notes
    -----
    This is an interface to the LAPACK routines sgerqf, dgerqf, cgerqf, zgerqf,
    sorgrq, dorgrq, cungrq and zungrq.

    If ``mode=economic``, the shapes of Q and R are (K, N) and (M, K) instead
    of (N,N) and (M,N), with ``K=min(M,N)``.

    Examples
    --------
    >>> from scipy import linalg
    >>> from numpy import random, dot, allclose
    >>> a = random.randn(6, 9)
    >>> r, q = linalg.rq(a)
    >>> allclose(a, dot(r, q))
    True
    >>> r.shape, q.shape
    ((6, 9), (9, 9))
    >>> r2 = linalg.rq(a, mode='r')
    >>> allclose(r, r2)
    True
    >>> r3, q3 = linalg.rq(a, mode='economic')
    >>> r3.shape, q3.shape
    ((6, 6), (6, 9))

    """
    if mode not in ['full', 'r', 'economic']:
        raise ValueError(
                 "Mode argument should be one of ['full', 'r', 'economic']")

    if check_finite:
        a1 = numpy.asarray_chkfinite(a)
    else:
        a1 = numpy.asarray(a)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    M, N = a1.shape
    overwrite_a = overwrite_a or (_datacopied(a1, a))

    gerqf, = get_lapack_funcs(('gerqf',), (a1,))
    if lwork is None or lwork == -1:
        # get optimal work array
        rq, tau, work, info = gerqf(a1, lwork=-1, overwrite_a=1)
        lwork = work[0].real.astype(numpy.int)
    rq, tau, work, info = gerqf(a1, lwork=lwork, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal gerqf'
                                                                    % -info)
    if not mode == 'economic' or N < M:
        R = numpy.triu(rq, N-M)
    else:
        R = numpy.triu(rq[-M:, -M:])

    if mode == 'r':
        return R

    gor_un_grq, = get_lapack_funcs(('orgrq',), (rq,))

    if N < M:
        # get optimal work array
        Q, work, info = gor_un_grq(rq[-N:], tau, lwork=-1, overwrite_a=1)
        lwork = work[0].real.astype(numpy.int)
        Q, work, info = gor_un_grq(rq[-N:], tau, lwork=lwork, overwrite_a=1)
    elif mode == 'economic':
        # get optimal work array
        Q, work, info = gor_un_grq(rq, tau, lwork=-1, overwrite_a=1)
        lwork = work[0].real.astype(numpy.int)
        Q, work, info = gor_un_grq(rq, tau, lwork=lwork, overwrite_a=1)
    else:
        rq1 = numpy.empty((N, N), dtype=rq.dtype)
        rq1[-M:] = rq
        # get optimal work array
        Q, work, info = gor_un_grq(rq1, tau, lwork=-1, overwrite_a=1)
        lwork = work[0].real.astype(numpy.int)
        Q, work, info = gor_un_grq(rq1, tau, lwork=lwork, overwrite_a=1)

    if info < 0:
        raise ValueError("illegal value in %d-th argument of internal orgrq"
                                                                    % -info)
    return R, Q
