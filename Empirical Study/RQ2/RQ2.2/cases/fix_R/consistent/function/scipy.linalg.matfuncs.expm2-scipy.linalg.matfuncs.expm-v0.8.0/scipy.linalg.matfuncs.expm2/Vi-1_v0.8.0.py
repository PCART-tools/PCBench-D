
def expm2(A):
    """Compute the matrix exponential using eigenvalue decomposition.

    Parameters
    ----------
    A : array, shape(M,M)
        Matrix to be exponentiated

    Returns
    -------
    expA : array, shape(M,M)
        Matrix exponential of A

    """
    A = asarray(A)
    t = A.dtype.char
    if t not in ['f','F','d','D']:
        A = A.astype('d')
        t = 'd'
    s,vr = eig(A)
    vri = inv(vr)
    return dot(dot(vr,diag(exp(s))),vri).astype(t)
