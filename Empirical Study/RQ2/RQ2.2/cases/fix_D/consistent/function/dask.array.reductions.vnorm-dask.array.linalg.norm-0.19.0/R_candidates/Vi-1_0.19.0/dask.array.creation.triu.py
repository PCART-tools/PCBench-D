def triu(m, k=0):
    """
    Upper triangle of an array with elements above the `k`-th diagonal zeroed.

    Parameters
    ----------
    m : array_like, shape (M, N)
        Input array.
    k : int, optional
        Diagonal above which to zero elements.  `k = 0` (the default) is the
        main diagonal, `k < 0` is below it and `k > 0` is above.

    Returns
    -------
    triu : ndarray, shape (M, N)
        Upper triangle of `m`, of same shape and data-type as `m`.

    See Also
    --------
    tril : lower triangle of an array
    """
    if m.ndim != 2:
        raise ValueError('input must be 2 dimensional')
    if m.chunks[0][0] != m.chunks[1][0]:
        msg = ('chunks must be a square. '
               'Use .rechunk method to change the size of chunks.')
        raise NotImplementedError(msg)

    rdim = len(m.chunks[0])
    hdim = len(m.chunks[1])
    chunk = m.chunks[0][0]

    token = tokenize(m, k)
    name = 'triu-' + token

    dsk = {}
    for i in range(rdim):
        for j in range(hdim):
            if chunk * (j - i + 1) < k:
                dsk[(name, i, j)] = (np.zeros, (m.chunks[0][i], m.chunks[1][j]))
            elif chunk * (j - i - 1) < k <= chunk * (j - i + 1):
                dsk[(name, i, j)] = (np.triu, (m.name, i, j), k - (chunk * (j - i)))
            else:
                dsk[(name, i, j)] = (m.name, i, j)
    return Array(sharedict.merge((name, dsk), m.dask), name,
                 shape=m.shape, chunks=m.chunks, dtype=m.dtype)
