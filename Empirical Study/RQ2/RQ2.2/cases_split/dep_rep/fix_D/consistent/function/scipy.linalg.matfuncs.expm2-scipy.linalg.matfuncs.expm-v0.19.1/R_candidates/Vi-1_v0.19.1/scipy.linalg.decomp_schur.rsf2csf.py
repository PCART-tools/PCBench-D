def rsf2csf(T, Z, check_finite=True):
    """
    Convert real Schur form to complex Schur form.

    Convert a quasi-diagonal real-valued Schur form to the upper triangular
    complex-valued Schur form.

    Parameters
    ----------
    T : (M, M) array_like
        Real Schur form of the original matrix
    Z : (M, M) array_like
        Schur transformation matrix
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    T : (M, M) ndarray
        Complex Schur form of the original matrix
    Z : (M, M) ndarray
        Schur transformation matrix corresponding to the complex form

    See also
    --------
    schur : Schur decompose a matrix

    """
    if check_finite:
        Z, T = map(asarray_chkfinite, (Z, T))
    else:
        Z,T = map(asarray, (Z,T))
    if len(Z.shape) != 2 or Z.shape[0] != Z.shape[1]:
        raise ValueError("matrix must be square.")
    if len(T.shape) != 2 or T.shape[0] != T.shape[1]:
        raise ValueError("matrix must be square.")
    if T.shape[0] != Z.shape[0]:
        raise ValueError("matrices must be same dimension.")
    N = T.shape[0]
    arr = numpy.array
    t = _commonType(Z, T, arr([3.0],'F'))
    Z, T = _castCopy(t, Z, T)
    conj = numpy.conj
    dot = numpy.dot
    r_ = numpy.r_
    transp = numpy.transpose
    for m in range(N-1, 0, -1):
        if abs(T[m,m-1]) > eps*(abs(T[m-1,m-1]) + abs(T[m,m])):
            k = slice(m-1, m+1)
            mu = eigvals(T[k,k]) - T[m,m]
            r = misc.norm([mu[0], T[m,m-1]])
            c = mu[0] / r
            s = T[m,m-1] / r
            G = r_[arr([[conj(c), s]], dtype=t), arr([[-s, c]], dtype=t)]
            Gc = conj(transp(G))
            j = slice(m-1, N)
            T[k,j] = dot(G, T[k,j])
            i = slice(0, m+1)
            T[i,k] = dot(T[i,k], Gc)
            i = slice(0, N)
            Z[i,k] = dot(Z[i,k], Gc)
        T[m,m-1] = 0.0
    return T, Z
