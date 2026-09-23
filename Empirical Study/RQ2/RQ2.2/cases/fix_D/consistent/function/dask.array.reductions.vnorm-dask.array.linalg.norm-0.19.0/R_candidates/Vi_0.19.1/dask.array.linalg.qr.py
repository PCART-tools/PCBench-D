def qr(a):
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
    dask.array.linalg.tsqr: Implementation for tall-and-skinny arrays
    dask.array.linalg.sfqr: Implementation for short-and-fat arrays
    """

    if len(a.chunks[1]) == 1 and len(a.chunks[0]) > 1:
        return tsqr(a)
    elif len(a.chunks[0]) == 1:
        return sfqr(a)
    else:
        raise NotImplementedError(
            "qr currently supports only tall-and-skinny (single column chunk/block; see tsqr)\n"
            "and short-and-fat (single row chunk/block; see sfqr) matrices\n\n"
            "Consider use of the rechunk method. For example,\n\n"
            "x.rechunk({0: -1, 1: 'auto'}) or x.rechunk({0: 'auto', 1: -1})\n\n"
            "which rechunk one shorter axis to a single chunk, while allowing\n"
            "the other axis to automatically grow/shrink appropriately."
        )
