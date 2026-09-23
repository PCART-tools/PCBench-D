def tril(m, k=0):
    """
    Lower triangle of an array with elements above the `k`-th diagonal zeroed.

    Parameters
    ----------
    m : array_like, shape (M, M)
        Input array.
    k : int, optional
        Diagonal above which to zero elements.  `k = 0` (the default) is the
        main diagonal, `k < 0` is below it and `k > 0` is above.

    Returns
    -------
    tril : ndarray, shape (M, M)
        Lower triangle of `m`, of same shape and data-type as `m`.

    See Also
    --------
    triu : upper triangle of an array
    """
    if m.ndim != 2:
        raise ValueError('input must be 2 dimensional')
    if m.shape[0] != m.shape[1]:
        raise NotImplementedError('input must be a square matrix')
    if not len(set(m.chunks[0] + m.chunks[1])) == 1:
        msg = ('All chunks must be a square matrix to perform lu decomposition. '
               'Use .rechunk method to change the size of chunks.')
        raise ValueError(msg)

    rdim = len(m.chunks[0])
    hdim = len(m.chunks[1])
    chunk = m.chunks[0][0]

    token = tokenize(m, k)
    name = 'tril-' + token

    dsk = {}
    for i in range(rdim):
        for j in range(hdim):
            if chunk * (j - i + 1) < k:
                dsk[(name, i, j)] = (m.name, i, j)
            elif chunk * (j - i - 1) < k <= chunk * (j - i + 1):
                dsk[(name, i, j)] = (np.tril, (m.name, i, j), k - (chunk * (j - i)))
            else:
                dsk[(name, i, j)] = (np.zeros, (m.chunks[0][i], m.chunks[1][j]))
    dsk.update(m.dask)
    return Array(dsk, name, shape=m.shape, chunks=m.chunks, dtype=m.dtype)
