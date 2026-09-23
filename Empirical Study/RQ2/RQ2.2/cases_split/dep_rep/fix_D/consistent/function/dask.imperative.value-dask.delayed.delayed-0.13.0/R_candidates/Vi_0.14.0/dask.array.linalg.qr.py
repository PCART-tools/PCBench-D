def qr(a, name=None):
    """
    Compute the qr factorization of a matrix.

    Examples
    --------

    >>> q, r = da.linalg.qr(x)  # doctest: +SKIP

    Returns
    -------

    q:  Array, orthonormal
    r:  Array, upper-triangular

    See Also
    --------

    np.linalg.qr : Equivalent NumPy Operation
    dask.array.linalg.tsqr: Actual implementation with citation
    """
    return tsqr(a, name)
