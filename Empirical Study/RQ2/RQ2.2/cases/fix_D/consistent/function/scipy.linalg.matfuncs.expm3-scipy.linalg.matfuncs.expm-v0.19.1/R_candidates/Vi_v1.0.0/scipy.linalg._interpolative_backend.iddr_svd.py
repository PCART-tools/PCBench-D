def iddr_svd(A, k):
    """
    Compute SVD of a real matrix to a specified rank.

    :param A:
        Matrix.
    :type A: :class:`numpy.ndarray`
    :param k:
        Rank of SVD.
    :type k: int

    :return:
        Left singular vectors.
    :rtype: :class:`numpy.ndarray`
    :return:
        Right singular vectors.
    :rtype: :class:`numpy.ndarray`
    :return:
        Singular values.
    :rtype: :class:`numpy.ndarray`
    """
    A = np.asfortranarray(A)
    U, V, S, ier = _id.iddr_svd(A, k)
    if ier:
        raise _RETCODE_ERROR
    return U, V, S
