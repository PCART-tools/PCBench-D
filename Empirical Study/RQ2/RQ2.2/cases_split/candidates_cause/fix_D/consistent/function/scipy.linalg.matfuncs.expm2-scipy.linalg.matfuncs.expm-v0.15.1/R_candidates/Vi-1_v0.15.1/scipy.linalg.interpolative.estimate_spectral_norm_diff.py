def estimate_spectral_norm_diff(A, B, its=20):
    """
    Estimate spectral norm of the difference of two matrices by the randomized
    power method.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`backend.idd_diffsnorm` and
        :func:`backend.idz_diffsnorm`.

    Parameters
    ----------
    A : :class:`scipy.sparse.linalg.LinearOperator`
        First matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with the
        `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
    B : :class:`scipy.sparse.linalg.LinearOperator`
        Second matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with
        the `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
    its : int
        Number of power method iterations.

    Returns
    -------
    float
        Spectral norm estimate of matrix difference.
    """
    from scipy.sparse.linalg import aslinearoperator
    A = aslinearoperator(A)
    B = aslinearoperator(B)
    m, n = A.shape
    matvec1 = lambda x: A. matvec(x)
    matveca1 = lambda x: A.rmatvec(x)
    matvec2 = lambda x: B. matvec(x)
    matveca2 = lambda x: B.rmatvec(x)
    if _is_real(A):
        return backend.idd_diffsnorm(
            m, n, matveca1, matveca2, matvec1, matvec2, its=its)
    else:
        return backend.idz_diffsnorm(
            m, n, matveca1, matveca2, matvec1, matvec2, its=its)
