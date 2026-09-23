def lu(a):
    """
    Compute the lu decomposition of a matrix.

    Examples
    --------

    >>> p, l, u = da.linalg.lu(x)  # doctest: +SKIP

    Returns
    -------

    p:  Array, permutation matrix
    l:  Array, lower triangular matrix with unit diagonal.
    u:  Array, upper triangular matrix
    """

    import scipy.linalg

    if a.ndim != 2:
        raise ValueError('Dimension must be 2 to perform lu decomposition')

    xdim, ydim = a.shape
    if xdim != ydim:
        raise ValueError('Input must be a square matrix to perform lu decomposition')
    if not len(set(a.chunks[0] + a.chunks[1])) == 1:
        msg = ('All chunks must be a square matrix to perform lu decomposition. '
               'Use .rechunk method to change the size of chunks.')
        raise ValueError(msg)

    vdim = len(a.chunks[0])
    hdim = len(a.chunks[1])

    token = tokenize(a)
    name_lu = 'lu-lu-' + token

    name_p = 'lu-p-' + token
    name_l = 'lu-l-' + token
    name_u = 'lu-u-' + token

    # for internal calculation
    name_p_inv = 'lu-p-inv-' + token
    name_l_permuted = 'lu-l-permute-' + token
    name_u_transposed = 'lu-u-transpose-' + token
    name_plu_dot = 'lu-plu-dot-' + token
    name_lu_dot = 'lu-lu-dot-' + token

    dsk = {}
    for i in range(min(vdim, hdim)):
        target = (a.name, i, i)
        if i > 0:
            prevs = []
            for p in range(i):
                prev = name_plu_dot, i, p, p, i
                dsk[prev] = (np.dot, (name_l_permuted, i, p), (name_u, p, i))
                prevs.append(prev)
            target = (operator.sub, target, (sum, prevs))
        # diagonal block
        dsk[name_lu, i, i] = (scipy.linalg.lu, target)

        # sweep to horizontal
        for j in range(i + 1, hdim):
            target = (np.dot, (name_p_inv, i, i), (a.name, i, j))
            if i > 0:
                prevs = []
                for p in range(i):
                    prev = name_lu_dot, i, p, p, j
                    dsk[prev] = (np.dot, (name_l, i, p), (name_u, p, j))
                    prevs.append(prev)
                target = (operator.sub, target, (sum, prevs))
            dsk[name_lu, i, j] = (_solve_triangular_lower,
                                  (name_l, i, i), target)

        # sweep to vertical
        for k in range(i + 1, vdim):
            target = (a.name, k, i)
            if i > 0:
                prevs = []
                for p in range(i):
                    prev = name_plu_dot, k, p, p, i
                    dsk[prev] = (np.dot, (name_l_permuted, k, p), (name_u, p, i))
                    prevs.append(prev)
                target = (operator.sub, target, (sum, prevs))
            # solving x.dot(u) = target is equal to u.T.dot(x.T) = target.T
            dsk[name_lu, k, i] = (np.transpose,
                                  (_solve_triangular_lower,
                                   (name_u_transposed, i, i),
                                   (np.transpose, target)))

    for i in range(min(vdim, hdim)):
        for j in range(min(vdim, hdim)):
            if i == j:
                dsk[name_p, i, j] = (operator.getitem, (name_lu, i, j), 0)
                dsk[name_l, i, j] = (operator.getitem, (name_lu, i, j), 1)
                dsk[name_u, i, j] = (operator.getitem, (name_lu, i, j), 2)

                # permuted l is required to be propagated to i > j blocks
                dsk[name_l_permuted, i, j] = (np.dot, (name_p, i, j), (name_l, i, j))
                dsk[name_u_transposed, i, j] = (np.transpose, (name_u, i, j))
                # transposed permutation matrix is equal to its inverse
                dsk[name_p_inv, i, j] = (np.transpose, (name_p, i, j))
            elif i > j:
                dsk[name_p, i, j] = (np.zeros, (a.chunks[0][i], a.chunks[1][j]))
                # calculations are performed using permuted l,
                # thus the result should be reverted by inverted (=transposed) p
                # to have the same row order as diagonal blocks
                dsk[name_l, i, j] = (np.dot, (name_p_inv, i, i), (name_lu, i, j))
                dsk[name_u, i, j] = (np.zeros, (a.chunks[0][i], a.chunks[1][j]))
                dsk[name_l_permuted, i, j] = (name_lu, i, j)
            else:
                dsk[name_p, i, j] = (np.zeros, (a.chunks[0][i], a.chunks[1][j]))
                dsk[name_l, i, j] = (np.zeros, (a.chunks[0][i], a.chunks[1][j]))
                dsk[name_u, i, j] = (name_lu, i, j)
                # l_permuted is not referred in upper triangulars

    dsk.update(a.dask)
    pp, ll, uu = scipy.linalg.lu(np.ones(shape=(1, 1), dtype=a.dtype))
    p = Array(dsk, name_p, shape=a.shape, chunks=a.chunks, dtype=pp.dtype)
    l = Array(dsk, name_l, shape=a.shape, chunks=a.chunks, dtype=ll.dtype)
    u = Array(dsk, name_u, shape=a.shape, chunks=a.chunks, dtype=uu.dtype)

    return p, l, u
