def svd(a):
    """
    Compute the singular value decomposition of a matrix.

    Examples
    --------

    >>> u, s, v = da.linalg.svd(x)  # doctest: +SKIP

    Returns
    -------

    u:  Array, unitary / orthogonal
    s:  Array, singular values in decreasing order (largest first)
    v:  Array, unitary / orthogonal

    See Also
    --------

    np.linalg.svd : Equivalent NumPy Operation
    dask.array.linalg.tsqr: Implementation for tall-and-skinny arrays
    """
    return tsqr(a, compute_svd=True)
