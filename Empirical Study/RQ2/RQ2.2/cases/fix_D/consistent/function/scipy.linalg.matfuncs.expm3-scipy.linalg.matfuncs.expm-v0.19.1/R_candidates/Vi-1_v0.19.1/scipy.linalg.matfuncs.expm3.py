@np.deprecate(new_name="expm")
def expm3(A, q=20):
    """
    Compute the matrix exponential using Taylor series.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix to be exponentiated
    q : int
        Order of the Taylor series used is `q-1`

    Returns
    -------
    expm3 : (N, N) ndarray
        Matrix exponential of `A`

    """
    A = _asarray_square(A)
    n = A.shape[0]
    t = A.dtype.char
    if t not in ['f','F','d','D']:
        A = A.astype('d')
        t = 'd'
    eA = np.identity(n, dtype=t)
    trm = np.identity(n, dtype=t)
    castfunc = cast[t]
    for k in range(1, q):
        trm[:] = trm.dot(A) / castfunc(k)
        eA += trm
    return eA
