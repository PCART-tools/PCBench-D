def svd(a, name=None):
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
    dask.array.linalg.tsqr: Actual implementation with citation
    """
    return tsqr(a, name, compute_svd=True)
