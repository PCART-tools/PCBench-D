def interp_decomp(A, eps_or_k, rand=True):
    """
    Compute ID of a matrix.

    An ID of a matrix `A` is a factorization defined by a rank `k`, a column
    index array `idx`, and interpolation coefficients `proj` such that::

        numpy.dot(A[:,idx[:k]], proj) = A[:,idx[k:]]

    The original matrix can then be reconstructed as::

        numpy.hstack([A[:,idx[:k]],
                                    numpy.dot(A[:,idx[:k]], proj)]
                                )[:,numpy.argsort(idx)]

    or via the routine :func:`reconstruct_matrix_from_id`. This can
    equivalently be written as::

        numpy.dot(A[:,idx[:k]],
                            numpy.hstack([numpy.eye(k), proj])
                          )[:,np.argsort(idx)]

    in terms of the skeleton and interpolation matrices::

        B = A[:,idx[:k]]

    and::

        P = numpy.hstack([numpy.eye(k), proj])[:,np.argsort(idx)]

    respectively. See also :func:`reconstruct_interp_matrix` and
    :func:`reconstruct_skel_matrix`.

    The ID can be computed to any relative precision or rank (depending on the
    value of `eps_or_k`). If a precision is specified (`eps_or_k < 1`), then
    this function has the output signature::

        k, idx, proj = interp_decomp(A, eps_or_k)

    Otherwise, if a rank is specified (`eps_or_k >= 1`), then the output
    signature is::

        idx, proj = interp_decomp(A, eps_or_k)

    ..  This function automatically detects the form of the input parameters
        and passes them to the appropriate backend. For details, see
        :func:`backend.iddp_id`, :func:`backend.iddp_aid`,
        :func:`backend.iddp_rid`, :func:`backend.iddr_id`,
        :func:`backend.iddr_aid`, :func:`backend.iddr_rid`,
        :func:`backend.idzp_id`, :func:`backend.idzp_aid`,
        :func:`backend.idzp_rid`, :func:`backend.idzr_id`,
        :func:`backend.idzr_aid`, and :func:`backend.idzr_rid`.

    Parameters
    ----------
    A : :class:`numpy.ndarray` or :class:`scipy.sparse.linalg.LinearOperator` with `rmatvec`
        Matrix to be factored
    eps_or_k : float or int
        Relative error (if `eps_or_k < 1`) or rank (if `eps_or_k >= 1`) of
        approximation.
    rand : bool, optional
        Whether to use random sampling if `A` is of type :class:`numpy.ndarray`
        (randomized algorithms are always used if `A` is of type
        :class:`scipy.sparse.linalg.LinearOperator`).

    Returns
    -------
    k : int
        Rank required to achieve specified relative precision if
        `eps_or_k < 1`.
    idx : :class:`numpy.ndarray`
        Column index array.
    proj : :class:`numpy.ndarray`
        Interpolation coefficients.
    """
    from scipy.sparse.linalg import LinearOperator

    real = _is_real(A)

    if isinstance(A, np.ndarray):
        if eps_or_k < 1:
            eps = eps_or_k
            if rand:
                if real:
                    k, idx, proj = backend.iddp_aid(eps, A)
                else:
                    k, idx, proj = backend.idzp_aid(eps, A)
            else:
                if real:
                    k, idx, proj = backend.iddp_id(eps, A)
                else:
                    k, idx, proj = backend.idzp_id(eps, A)
            return k, idx - 1, proj
        else:
            k = int(eps_or_k)
            if rand:
                if real:
                    idx, proj = backend.iddr_aid(A, k)
                else:
                    idx, proj = backend.idzr_aid(A, k)
            else:
                if real:
                    idx, proj = backend.iddr_id(A, k)
                else:
                    idx, proj = backend.idzr_id(A, k)
            return idx - 1, proj
    elif isinstance(A, LinearOperator):
        m, n = A.shape
        matveca = A.rmatvec
        if eps_or_k < 1:
            eps = eps_or_k
            if real:
                k, idx, proj = backend.iddp_rid(eps, m, n, matveca)
            else:
                k, idx, proj = backend.idzp_rid(eps, m, n, matveca)
            return k, idx - 1, proj
        else:
            k = int(eps_or_k)
            if real:
                idx, proj = backend.iddr_rid(m, n, matveca, k)
            else:
                idx, proj = backend.idzr_rid(m, n, matveca, k)
            return idx - 1, proj
    else:
        raise _TYPE_ERROR
