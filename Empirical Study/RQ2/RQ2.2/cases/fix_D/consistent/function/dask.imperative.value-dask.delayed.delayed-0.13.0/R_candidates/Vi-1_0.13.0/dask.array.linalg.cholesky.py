def cholesky(a, lower=False):
    """
    Returns the Cholesky decomposition, :math:`A = L L^*` or
    :math:`A = U^* U` of a Hermitian positive-definite matrix A.

    Parameters
    ----------
    a : (M, M) array_like
        Matrix to be decomposed
    lower : bool, optional
        Whether to compute the upper or lower triangular Cholesky
        factorization.  Default is upper-triangular.

    Returns
    -------
    c : (M, M) Array
        Upper- or lower-triangular Cholesky factor of `a`.
    """

    l, u = _cholesky(a)
    if lower:
        return l
    else:
        return u
