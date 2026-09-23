def transpose(A):
    """Return transpose of a matrix or batches of matrices.
    """
    ndim = len(A.shape)
    return A.transpose(ndim - 1, ndim - 2)
