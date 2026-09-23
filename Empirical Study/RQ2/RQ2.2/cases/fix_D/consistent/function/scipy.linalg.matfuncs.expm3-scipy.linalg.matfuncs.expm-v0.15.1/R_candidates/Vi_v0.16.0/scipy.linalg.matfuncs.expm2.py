@np.deprecate(new_name="expm")
def expm2(A):
    """
    Compute the matrix exponential using eigenvalue decomposition.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix to be exponentiated

    Returns
    -------
    expm2 : (N, N) ndarray
        Matrix exponential of `A`

    """
    A = _asarray_square(A)
    t = A.dtype.char
    if t not in ['f','F','d','D']:
        A = A.astype('d')
        t = 'd'
    s, vr = eig(A)
    vri = inv(vr)
    r = dot(dot(vr, diag(exp(s))), vri)
    if t in ['f', 'd']:
        return r.real.astype(t)
    else:
        return r.astype(t)
