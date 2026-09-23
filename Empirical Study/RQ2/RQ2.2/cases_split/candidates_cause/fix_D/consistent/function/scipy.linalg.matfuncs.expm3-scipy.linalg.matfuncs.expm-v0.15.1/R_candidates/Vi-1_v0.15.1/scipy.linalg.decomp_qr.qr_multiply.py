def qr_multiply(a, c, mode='right', pivoting=False, conjugate=False,
    overwrite_a=False, overwrite_c=False):
    """
    Calculate the QR decomposition and multiply Q with a matrix.

    Calculate the decomposition ``A = Q R`` where Q is unitary/orthogonal
    and R upper triangular. Multiply Q with a vector or a matrix c.

    Parameters
    ----------
    a : ndarray, shape (M, N)
        Matrix to be decomposed
    c : ndarray, one- or two-dimensional
        calculate the product of c and q, depending on the mode:
    mode : {'left', 'right'}, optional
        ``dot(Q, c)`` is returned if mode is 'left',
        ``dot(c, Q)`` is returned if mode is 'right'.
        The shape of c must be appropriate for the matrix multiplications,
        if mode is 'left', ``min(a.shape) == c.shape[0]``,
        if mode is 'right', ``a.shape[0] == c.shape[1]``.
    pivoting : bool, optional
        Whether or not factorization should include pivoting for rank-revealing
        qr decomposition, see the documentation of qr.
    conjugate : bool, optional
        Whether Q should be complex-conjugated. This might be faster
        than explicit conjugation.
    overwrite_a : bool, optional
        Whether data in a is overwritten (may improve performance)
    overwrite_c : bool, optional
        Whether data in c is overwritten (may improve performance).
        If this is used, c must be big enough to keep the result,
        i.e. c.shape[0] = a.shape[0] if mode is 'left'.


    Returns
    -------
    CQ : float or complex ndarray
        the product of Q and c, as defined in mode
    R : float or complex ndarray
        Of shape (K, N), ``K = min(M, N)``.
    P : ndarray of ints
        Of shape (N,) for ``pivoting=True``.
        Not returned if ``pivoting=False``.

    Raises
    ------
    LinAlgError
        Raised if decomposition fails

    Notes
    -----
    This is an interface to the LAPACK routines dgeqrf, zgeqrf,
    dormqr, zunmqr, dgeqp3, and zgeqp3.

    .. versionadded:: 0.11.0

    """
    if mode not in ['left', 'right']:
        raise ValueError("Mode argument should be one of ['left', 'right']")
    c = numpy.asarray_chkfinite(c)
    onedim = c.ndim == 1
    if onedim:
        c = c.reshape(1, len(c))
        if mode == "left":
            c = c.T

    a = numpy.asarray(a)  # chkfinite done in qr
    M, N = a.shape
    if not (mode == "left" and
                (not overwrite_c and min(M, N) == c.shape[0] or
                     overwrite_c and M == c.shape[0]) or
            mode == "right" and M == c.shape[1]):
        raise ValueError("objects are not aligned")

    raw = qr(a, overwrite_a, None, "raw", pivoting)
    Q, tau = raw[0]

    gor_un_mqr, = get_lapack_funcs(('ormqr',), (Q,))
    if gor_un_mqr.typecode in ('s', 'd'):
        trans = "T"
    else:
        trans = "C"

    Q = Q[:, :min(M, N)]
    if M > N and mode == "left" and not overwrite_c:
        if conjugate:
            cc = numpy.zeros((c.shape[1], M), dtype=c.dtype, order="F")
            cc[:, :N] = c.T
        else:
            cc = numpy.zeros((M, c.shape[1]), dtype=c.dtype, order="F")
            cc[:N, :] = c
            trans = "N"
        if conjugate:
            lr = "R"
        else:
            lr = "L"
        overwrite_c = True
    elif c.flags["C_CONTIGUOUS"] and trans == "T" or conjugate:
        cc = c.T
        if mode == "left":
            lr = "R"
        else:
            lr = "L"
    else:
        trans = "N"
        cc = c
        if mode == "left":
            lr = "L"
        else:
            lr = "R"
    cQ, = safecall(gor_un_mqr, "gormqr/gunmqr", lr, trans, Q, tau, cc,
            overwrite_c=overwrite_c)
    if trans != "N":
        cQ = cQ.T
    if mode == "right":
        cQ = cQ[:, :min(M, N)]
    if onedim:
        cQ = cQ.ravel()

    return (cQ,) + raw[1:]
