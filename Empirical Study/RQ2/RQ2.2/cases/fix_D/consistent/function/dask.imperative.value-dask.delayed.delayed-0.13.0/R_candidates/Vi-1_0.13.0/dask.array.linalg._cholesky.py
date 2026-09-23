def _cholesky(a):
    """
    Private function to perform Cholesky decomposition, which returns both
    lower and upper triangulars.
    """
    import scipy.linalg

    if a.ndim != 2:
        raise ValueError('Dimension must be 2 to perform cholesky decomposition')

    xdim, ydim = a.shape
    if xdim != ydim:
        raise ValueError('Input must be a square matrix to perform cholesky decomposition')
    if not len(set(a.chunks[0] + a.chunks[1])) == 1:
        msg = ('All chunks must be a square matrix to perform cholesky decomposition. '
               'Use .rechunk method to change the size of chunks.')
        raise ValueError(msg)

    vdim = len(a.chunks[0])
    hdim = len(a.chunks[1])

    token = tokenize(a)
    name = 'cholesky-' + token

    # (name_lt_dot, i, j, k, l) corresponds to l_ij.dot(l_kl.T)
    name_lt_dot = 'cholesky-lt-dot-' + token
    # because transposed results are needed for calculation,
    # we can build graph for upper triangular simultaneously
    name_upper = 'cholesky-upper-' + token

    # calculates lower triangulars because subscriptions get simpler
    dsk = {}
    for i in range(vdim):
        for j in range(hdim):
            if i < j:
                dsk[name, i, j] = (np.zeros, (a.chunks[0][i], a.chunks[1][j]))
                dsk[name_upper, j, i] = (name, i, j)
            elif i == j:
                target = (a.name, i, j)
                if i > 0:
                    prevs = []
                    for p in range(i):
                        prev = name_lt_dot, i, p, i, p
                        dsk[prev] = (np.dot, (name, i, p), (name_upper, p, i))
                        prevs.append(prev)
                    target = (operator.sub, target, (sum, prevs))
                dsk[name, i, i] = (_cholesky_lower, target)
                dsk[name_upper, i, i] = (np.transpose, (name, i, i))
            else:
                # solving x.dot(L11.T) = (A21 - L20.dot(L10.T)) is equal to
                # L11.dot(x.T) = A21.T - L10.dot(L20.T)
                # L11.dot(x.T) = A12 - L10.dot(L02)
                target = (a.name, j, i)
                if j > 0:
                    prevs = []
                    for p in range(j):
                        prev = name_lt_dot, j, p, i, p
                        dsk[prev] = (np.dot, (name, j, p), (name_upper, p, i))
                        prevs.append(prev)
                    target = (operator.sub, target, (sum, prevs))
                dsk[name_upper, j, i] = (_solve_triangular_lower,(name, j, j), target)
                dsk[name, i, j] = (np.transpose, (name_upper, j, i))

    dsk.update(a.dask)
    cho = scipy.linalg.cholesky(np.array([[1, 2], [2, 5]], dtype=a.dtype))

    lower = Array(dsk, name, shape=a.shape, chunks=a.chunks, dtype=cho.dtype)
    # do not use .T, because part of transposed blocks are already calculated
    upper = Array(dsk, name_upper, shape=a.shape, chunks=a.chunks, dtype=cho.dtype)
    return lower, upper
