def svd(A, eps_or_k, rand=True):
    """
    Compute SVD of a matrix via an ID.

    An SVD of a matrix `A` is a factorization::

        A = numpy.dot(U, numpy.dot(numpy.diag(S), V.conj().T))

    where `U` and `V` have orthonormal columns and `S` is nonnegative.

    The SVD can be computed to any relative precision or rank (depending on the
    value of `eps_or_k`).

    See also :func:`interp_decomp` and :func:`id_to_svd`.

    ..  This function automatically detects the form of the input parameters and
        passes them to the appropriate backend. For details, see
        :func:`backend.iddp_svd`, :func:`backend.iddp_asvd`,
        :func:`backend.iddp_rsvd`, :func:`backend.iddr_svd`,
        :func:`backend.iddr_asvd`, :func:`backend.iddr_rsvd`,
        :func:`backend.idzp_svd`, :func:`backend.idzp_asvd`,
        :func:`backend.idzp_rsvd`, :func:`backend.idzr_svd`,
        :func:`backend.idzr_asvd`, and :func:`backend.idzr_rsvd`.

    Parameters
    ----------
    A : :class:`numpy.ndarray` or :class:`scipy.sparse.linalg.LinearOperator`
        Matrix to be factored, given as either a :class:`numpy.ndarray` or a
        :class:`scipy.sparse.linalg.LinearOperator` with the `matvec` and
        `rmatvec` methods (to apply the matrix and its adjoint).
    eps_or_k : float or int
        Relative error (if `eps_or_k < 1`) or rank (if `eps_or_k >= 1`) of
        approximation.
    rand : bool, optional
        Whether to use random sampling if `A` is of type :class:`numpy.ndarray`
        (randomized algorithms are always used if `A` is of type
        :class:`scipy.sparse.linalg.LinearOperator`).

    Returns
    -------
    U : :class:`numpy.ndarray`
        Left singular vectors.
    S : :class:`numpy.ndarray`
        Singular values.
    V : :class:`numpy.ndarray`
        Right singular vectors.
    """
    from scipy.sparse.linalg import LinearOperator

    real = _is_real(A)

    if isinstance(A, np.ndarray):
        if eps_or_k < 1:
            eps = eps_or_k
            if rand:
                if real:
                    U, V, S = backend.iddp_asvd(eps, A)
                else:
                    U, V, S = backend.idzp_asvd(eps, A)
            else:
                if real:
                    U, V, S = backend.iddp_svd(eps, A)
                else:
                    U, V, S = backend.idzp_svd(eps, A)
        else:
            k = int(eps_or_k)
            if rand:
                if real:
                    U, V, S = backend.iddr_asvd(A, k)
                else:
                    U, V, S = backend.idzr_asvd(A, k)
            else:
                if real:
                    U, V, S = backend.iddr_svd(A, k)
                else:
                    U, V, S = backend.idzr_svd(A, k)
    elif isinstance(A, LinearOperator):
        m, n = A.shape
        matvec = lambda x: A.matvec(x)
        matveca = lambda x: A.rmatvec(x)
        if eps_or_k < 1:
            eps = eps_or_k
            if real:
                U, V, S = backend.iddp_rsvd(eps, m, n, matveca, matvec)
            else:
                U, V, S = backend.idzp_rsvd(eps, m, n, matveca, matvec)
        else:
            k = int(eps_or_k)
            if real:
                U, V, S = backend.iddr_rsvd(m, n, matveca, matvec, k)
            else:
                U, V, S = backend.idzr_rsvd(m, n, matveca, matvec, k)
    else:
        raise _TYPE_ERROR
    return U, S, V
