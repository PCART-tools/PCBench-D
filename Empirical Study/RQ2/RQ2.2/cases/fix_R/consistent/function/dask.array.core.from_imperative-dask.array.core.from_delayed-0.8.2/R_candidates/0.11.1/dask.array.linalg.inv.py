def inv(a):
    """
    Compute the inverse of a matrix with LU decomposition and
    forward / backward substitutions.

    Parameters
    ----------
    a : array_like
        Square matrix to be inverted.

    Returns
    -------
    ainv : Array
        Inverse of the matrix `a`.
    """
    return solve(a, eye(a.shape[0], chunks=a.chunks[0][0]))
