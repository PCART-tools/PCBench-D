def expm3(A, q=20):
    """
    Compute the matrix exponential using Taylor series.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix to be exponentiated
    q : int
        Order of the Taylor series

    Returns
    -------
    expm3 : (N, N) ndarray
        Matrix exponential of `A`

    """
    A = asarray(A)
    t = A.dtype.char
    if t not in ['f','F','d','D']:
        A = A.astype('d')
        t = 'd'
    A = mat(A)
    eA = eye(*A.shape,**{'dtype':t})
    trm = mat(eA, copy=True)
    castfunc = cast[t]
    for k in range(1,q):
        trm *= A / castfunc(k)
        eA += trm
    return eA
