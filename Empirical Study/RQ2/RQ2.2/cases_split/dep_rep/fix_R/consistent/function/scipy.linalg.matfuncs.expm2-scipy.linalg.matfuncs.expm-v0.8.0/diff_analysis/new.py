
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
    r = dot(dot(vr,diag(exp(s))),vri)
    if t in ['f', 'd']:
        return r.real.astype(t)
    else:
        return r.astype(t)
