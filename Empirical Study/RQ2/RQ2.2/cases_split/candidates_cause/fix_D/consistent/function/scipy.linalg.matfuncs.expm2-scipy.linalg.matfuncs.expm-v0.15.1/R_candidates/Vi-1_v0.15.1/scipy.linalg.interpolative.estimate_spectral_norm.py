def estimate_spectral_norm(A, its=20):
    """
    Estimate spectral norm of a matrix by the randomized power method.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`backend.idd_snorm` and
        :func:`backend.idz_snorm`.

    Parameters
    ----------
    A : :class:`scipy.sparse.linalg.LinearOperator`
        Matrix given as a :class:`scipy.sparse.linalg.LinearOperator` with the
        `matvec` and `rmatvec` methods (to apply the matrix and its adjoint).
    its : int
        Number of power method iterations.

    Returns
    -------
    float
        Spectral norm estimate.
    """
    from scipy.sparse.linalg import aslinearoperator
    A = aslinearoperator(A)
    m, n = A.shape
    matvec = lambda x: A. matvec(x)
    matveca = lambda x: A.rmatvec(x)
    if _is_real(A):
        return backend.idd_snorm(m, n, matveca, matvec, its=its)
    else:
        return backend.idz_snorm(m, n, matveca, matvec, its=its)
