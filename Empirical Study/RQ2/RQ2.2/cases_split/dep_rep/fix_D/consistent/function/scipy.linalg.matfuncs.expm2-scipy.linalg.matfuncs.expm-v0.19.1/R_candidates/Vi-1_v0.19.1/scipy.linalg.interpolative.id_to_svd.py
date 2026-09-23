def id_to_svd(B, idx, proj):
    """
    Convert ID to SVD.

    The SVD reconstruction of a matrix with skeleton matrix `B` and ID indices and
    coefficients `idx` and `proj`, respectively, is::

        U, S, V = id_to_svd(B, idx, proj)
        A = numpy.dot(U, numpy.dot(numpy.diag(S), V.conj().T))

    See also :func:`svd`.

    ..  This function automatically detects the matrix data type and calls the
        appropriate backend. For details, see :func:`backend.idd_id2svd` and
        :func:`backend.idz_id2svd`.

    Parameters
    ----------
    B : :class:`numpy.ndarray`
        Skeleton matrix.
    idx : :class:`numpy.ndarray`
        Column index array.
    proj : :class:`numpy.ndarray`
        Interpolation coefficients.

    Returns
    -------
    U : :class:`numpy.ndarray`
        Left singular vectors.
    S : :class:`numpy.ndarray`
        Singular values.
    V : :class:`numpy.ndarray`
        Right singular vectors.
    """
    if _is_real(B):
        U, V, S = backend.idd_id2svd(B, idx + 1, proj)
    else:
        U, V, S = backend.idz_id2svd(B, idx + 1, proj)
    return U, S, V
