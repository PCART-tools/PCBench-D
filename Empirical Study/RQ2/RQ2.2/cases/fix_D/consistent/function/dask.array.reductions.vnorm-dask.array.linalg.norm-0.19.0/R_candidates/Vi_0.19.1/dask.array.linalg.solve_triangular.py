def solve_triangular(a, b, lower=False):
    """
    Solve the equation `a x = b` for `x`, assuming a is a triangular matrix.

    Parameters
    ----------
    a : (M, M) array_like
        A triangular matrix
    b : (M,) or (M, N) array_like
        Right-hand side matrix in `a x = b`
    lower : bool, optional
        Use only data contained in the lower triangle of `a`.
        Default is to use upper triangle.

    Returns
    -------
    x : (M,) or (M, N) array
        Solution to the system `a x = b`. Shape of return matches `b`.
    """

    import scipy.linalg

    if a.ndim != 2:
        raise ValueError('a must be 2 dimensional')
    if b.ndim <= 2:
        if a.shape[1] != b.shape[0]:
            raise ValueError('a.shape[1] and b.shape[0] must be equal')
        if a.chunks[1] != b.chunks[0]:
            msg = ('a.chunks[1] and b.chunks[0] must be equal. '
                   'Use .rechunk method to change the size of chunks.')
            raise ValueError(msg)
    else:
        raise ValueError('b must be 1 or 2 dimensional')

    vchunks = len(a.chunks[1])
    hchunks = 1 if b.ndim == 1 else len(b.chunks[1])
    token = tokenize(a, b, lower)
    name = 'solve-triangular-' + token

    # for internal calculation
    # (name, i, j, k, l) corresponds to a_ij.dot(b_kl)
    name_mdot = 'solve-tri-dot-' + token

    def _b_init(i, j):
        if b.ndim == 1:
            return b.name, i
        else:
            return b.name, i, j

    def _key(i, j):
        if b.ndim == 1:
            return name, i
        else:
            return name, i, j

    dsk = {}
    if lower:
        for i in range(vchunks):
            for j in range(hchunks):
                target = _b_init(i, j)
                if i > 0:
                    prevs = []
                    for k in range(i):
                        prev = name_mdot, i, k, k, j
                        dsk[prev] = (np.dot, (a.name, i, k), _key(k, j))
                        prevs.append(prev)
                    target = (operator.sub, target, (sum, prevs))
                dsk[_key(i, j)] = (_solve_triangular_lower, (a.name, i, i), target)
    else:
        for i in range(vchunks):
            for j in range(hchunks):
                target = _b_init(i, j)
                if i < vchunks - 1:
                    prevs = []
                    for k in range(i + 1, vchunks):
                        prev = name_mdot, i, k, k, j
                        dsk[prev] = (np.dot, (a.name, i, k), _key(k, j))
                        prevs.append(prev)
                    target = (operator.sub, target, (sum, prevs))
                dsk[_key(i, j)] = (scipy.linalg.solve_triangular, (a.name, i, i), target)

    dsk = sharedict.merge(a.dask, b.dask, (name, dsk))
    res = _solve_triangular_lower(np.array([[1, 0], [1, 2]], dtype=a.dtype),
                                  np.array([0, 1], dtype=b.dtype))
    return Array(dsk, name, shape=b.shape, chunks=b.chunks, dtype=res.dtype)
