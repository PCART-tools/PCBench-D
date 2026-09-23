def vec(M):
    """
    Stack columns of M to construct a single vector.

    This is somewhat standard notation in linear algebra.

    Parameters
    ----------
    M : 2d array-like
        Input matrix
    
    Returns
    -------
    v : 1d ndarray
        Output vector

    """
    return M.T.ravel()
