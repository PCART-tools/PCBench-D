def tsqr(data, compute_svd=False, _max_vchunk_size=None):
    """ Direct Tall-and-Skinny QR algorithm

    As presented in:

        A. Benson, D. Gleich, and J. Demmel.
        Direct QR factorizations for tall-and-skinny matrices in
        MapReduce architectures.
        IEEE International Conference on Big Data, 2013.
        http://arxiv.org/abs/1301.1071

    This algorithm is used to compute both the QR decomposition and the
    Singular Value Decomposition.  It requires that the input array have a
    single column of blocks, each of which fit in memory.

    Parameters
    ----------
    data: Array
    compute_svd: bool
        Whether to compute the SVD rather than the QR decomposition
    _max_vchunk_size: Integer
        Used internally in recursion to set the maximum row dimension
        of chunks in subsequent recursive calls.

    Notes
    -----
    With ``k`` blocks of size ``(m, n)``, this algorithm has memory use that
    scales as ``k * m * n``.

    The implementation here is the recursive variant due to the ultimate
    need for one "single core" QR decomposition. In the non-recursive version
    of the algorithm, given ``k`` blocks, after ``k`` ``m * n`` QR
    decompositions, there will be a "single core" QR decomposition that will
    have to work with a ``(k * n, n)`` matrix.

    Here, recursion is applied as necessary to ensure that ``k * n`` is not
    larger than ``m`` (if ``m / n >= 2``). In particular, this is done
    to ensure that single core computations do not have to work on blocks
    larger than ``(m, n)``.

    Where blocks are irregular, the above logic is applied with the "height" of
    the "tallest" block used in place of ``m``.

    Consider use of the ``rechunk`` method to control this behavior. Blocks
    that are as tall as possible are recommended.

    See Also
    --------
    dask.array.linalg.qr - Powered by this algorithm
    dask.array.linalg.svd - Powered by this algorithm
    dask.array.linalg.sfqr - Variant for short-and-fat arrays
    """
    nr, nc = len(data.chunks[0]), len(data.chunks[1])
    cr_max, cc = max(data.chunks[0]), data.chunks[1][0]

    if not (data.ndim == 2 and  # Is a matrix
            nc == 1):           # Only one column block
        raise ValueError(
            "Input must have the following properties:\n"
            "  1. Have two dimensions\n"
            "  2. Have only one column of blocks\n\n"
            "Note: This function (tsqr) supports QR decomposition in the case of\n"
            "tall-and-skinny matrices (single column chunk/block; see qr)"
        )

    token = '-' + tokenize(data, compute_svd)

    m, n = data.shape
    numblocks = (nr, 1)

    qq, rr = np.linalg.qr(np.ones(shape=(1, 1), dtype=data.dtype))

    dsk = sharedict.ShareDict()
    dsk.update(data.dask)

    # Block qr
    name_qr_st1 = 'qr' + token
    dsk_qr_st1 = top(_wrapped_qr, name_qr_st1, 'ij', data.name, 'ij',
                     numblocks={data.name: numblocks})
    dsk.update_with_key(dsk_qr_st1, key=name_qr_st1)

    # Block qr[0]
    name_q_st1 = 'getitem' + token + '-q1'
    dsk_q_st1 = dict(((name_q_st1, i, 0),
                      (operator.getitem, (name_qr_st1, i, 0), 0))
                     for i in range(numblocks[0]))
    dsk.update_with_key(dsk_q_st1, key=name_q_st1)

    # Block qr[1]
    name_r_st1 = 'getitem' + token + '-r1'
    dsk_r_st1 = dict(((name_r_st1, i, 0),
                      (operator.getitem, (name_qr_st1, i, 0), 1))
                     for i in range(numblocks[0]))
    dsk.update_with_key(dsk_r_st1, key=name_r_st1)

    # Next step is to obtain a QR decomposition for the stacked R factors, so either:
    # - gather R factors into a single core and do a QR decomposition
    # - recurse with tsqr (if single core computation too large and a-priori "meaningful
    #   reduction" possible, meaning that chunks have to be well defined)

    single_core_compute_m = nr * cc
    chunks_well_defined = not any(np.isnan(c) for cs in data.chunks for c in cs)
    prospective_blocks = np.ceil(single_core_compute_m / cr_max)
    meaningful_reduction_possible = (cr_max if _max_vchunk_size is None else _max_vchunk_size) >= 2 * cc
    can_distribute = chunks_well_defined and int(prospective_blocks) > 1

    if chunks_well_defined and meaningful_reduction_possible and can_distribute:
        # stack chunks into blocks and recurse using tsqr

        # Prepare to stack chunks into blocks (from block qr[1])
        all_blocks = []
        curr_block = []
        curr_block_sz = 0
        for idx, a_m in enumerate(data.chunks[0]):
            m_q = a_m
            n_q = min(m_q, cc)
            m_r = n_q
            # n_r = cc
            if curr_block_sz + m_r > cr_max:
                all_blocks.append(curr_block)
                curr_block = []
                curr_block_sz = 0
            curr_block.append((idx, m_r))
            curr_block_sz += m_r
        if len(curr_block) > 0:
            all_blocks.append(curr_block)

        # R_stacked
        name_r_stacked = 'stack' + token + '-r1'
        dsk_r_stacked = dict(((name_r_stacked, i, 0),
                              (np.vstack, (tuple,
                                           [(name_r_st1, idx, 0)
                                            for idx, _ in sub_block_info])))
                             for i, sub_block_info in enumerate(all_blocks))
        dsk.update_with_key(dsk_r_stacked, key=name_r_stacked)

        # retrieve R_stacked for recursion with tsqr
        vchunks_rstacked = tuple([sum(map(lambda x: x[1], sub_block_info)) for sub_block_info in all_blocks])
        r_stacked = Array(dsk, name_r_stacked,
                          shape=(sum(vchunks_rstacked), n), chunks=(vchunks_rstacked, (n)), dtype=rr.dtype)

        # recurse
        q_inner, r_inner = tsqr(r_stacked, _max_vchunk_size=cr_max)
        dsk.update(q_inner.dask)
        dsk.update(r_inner.dask)

        # Q_inner: "unstack"
        name_q_st2 = 'getitem-' + token + '-q2'
        dsk_q_st2 = dict(((name_q_st2, j, 0),
                          (operator.getitem,
                           (q_inner.name, i, 0),
                           ((slice(e[0], e[1])), (slice(0, n)))))
                         for i, sub_block_info in enumerate(all_blocks)
                         for j, e in zip([x[0] for x in sub_block_info],
                                         _cumsum_blocks([x[1] for x in sub_block_info])))
        dsk.update_with_key(dsk_q_st2, key=name_q_st2)

        # R: R_inner
        name_r_st2 = 'r-inner-' + token
        dsk_r_st2 = {(name_r_st2, 0, 0): (r_inner.name, 0, 0)}
        dsk.update_with_key(dsk_r_st2, key=name_r_st2)

        # Q: Block qr[0] (*) Q_inner
        name_q_st3 = 'dot-' + token + '-q3'
        dsk_q_st3 = top(np.dot, name_q_st3, 'ij', name_q_st1, 'ij',
                        name_q_st2, 'ij', numblocks={name_q_st1: numblocks,
                                                     name_q_st2: numblocks})
        dsk.update_with_key(dsk_q_st3, key=name_q_st3)
    else:
        # Do single core computation

        # Stacking for in-core QR computation
        to_stack = [(name_r_st1, i, 0) for i in range(numblocks[0])]
        name_r_st1_stacked = 'stack' + token + '-r1'
        dsk_r_st1_stacked = {(name_r_st1_stacked, 0, 0): (np.vstack,
                                                          (tuple, to_stack))}
        dsk.update_with_key(dsk_r_st1_stacked, key=name_r_st1_stacked)

        # In-core QR computation
        name_qr_st2 = 'qr' + token + '-qr2'
        dsk_qr_st2 = top(np.linalg.qr, name_qr_st2, 'ij', name_r_st1_stacked, 'ij',
                         numblocks={name_r_st1_stacked: (1, 1)})
        dsk.update_with_key(dsk_qr_st2, key=name_qr_st2)

        # In-core qr[0]
        name_q_st2_aux = 'getitem' + token + '-q2-aux'
        dsk_q_st2_aux = {(name_q_st2_aux, 0, 0): (operator.getitem,
                                                  (name_qr_st2, 0, 0), 0)}
        dsk.update_with_key(dsk_q_st2_aux, key=name_q_st2_aux)

        if not any(np.isnan(c) for cs in data.chunks for c in cs):
            # when chunks are all known...
            # obtain slices on q from in-core compute (e.g.: (slice(10, 20), slice(0, 5)))
            q2_block_sizes = [min(e, n) for e in data.chunks[0]]
            block_slices = [(slice(e[0], e[1]), slice(0, n))
                            for e in _cumsum_blocks(q2_block_sizes)]
            dsk_q_blockslices = {}
        else:
            # when chunks are not already known...

            # request shape information: vertical chunk sizes & column dimension (n)
            name_q2bs = 'shape' + token + '-q2'
            dsk_q2_shapes = {(name_q2bs, i): (min, (getattr, (data.name, i, 0), 'shape'))
                             for i in range(numblocks[0])}
            name_n = 'getitem' + token + '-n'
            dsk_n = {name_n: (operator.getitem,
                              (getattr, (data.name, 0, 0), 'shape'), 1)}

            # cumulative sums (start, end)
            name_q2cs = 'cumsum' + token + '-q2'
            dsk_q2_cumsum = {(name_q2cs, 0): [0, (name_q2bs, 0)]}
            dsk_q2_cumsum.update({(name_q2cs, i): (_cumsum_part,
                                                   (name_q2cs, i - 1),
                                                   (name_q2bs, i))
                                  for i in range(1, numblocks[0])})

            # obtain slices on q from in-core compute (e.g.: (slice(10, 20), slice(0, 5)))
            name_blockslice = 'slice' + token + '-q'
            dsk_block_slices = {(name_blockslice, i): (tuple, [
                (apply, slice, (name_q2cs, i)), (slice, 0, name_n)])
                for i in range(numblocks[0])}

            dsk_q_blockslices = toolz.merge(dsk_n,
                                            dsk_q2_shapes,
                                            dsk_q2_cumsum,
                                            dsk_block_slices)

            block_slices = [(name_blockslice, i) for i in range(numblocks[0])]

        dsk.update_with_key(dsk_q_blockslices, key='q-blocksizes' + token)

        # In-core qr[0] unstacking
        name_q_st2 = 'getitem' + token + '-q2'
        dsk_q_st2 = dict(((name_q_st2, i, 0),
                          (operator.getitem, (name_q_st2_aux, 0, 0), b))
                         for i, b in enumerate(block_slices))
        dsk.update_with_key(dsk_q_st2, key=name_q_st2)

        # Q: Block qr[0] (*) In-core qr[0]
        name_q_st3 = 'dot' + token + '-q3'
        dsk_q_st3 = top(np.dot, name_q_st3, 'ij', name_q_st1, 'ij',
                        name_q_st2, 'ij', numblocks={name_q_st1: numblocks,
                                                     name_q_st2: numblocks})
        dsk.update_with_key(dsk_q_st3, key=name_q_st3)

        # R: In-core qr[1]
        name_r_st2 = 'getitem' + token + '-r2'
        dsk_r_st2 = {(name_r_st2, 0, 0): (operator.getitem, (name_qr_st2, 0, 0), 1)}
        dsk.update_with_key(dsk_r_st2, key=name_r_st2)

    if not compute_svd:
        is_unknown_m = np.isnan(data.shape[0]) or any(np.isnan(c) for c in data.chunks[0])
        is_unknown_n = np.isnan(data.shape[1]) or any(np.isnan(c) for c in data.chunks[1])

        if is_unknown_m and is_unknown_n:
            # assumption: m >= n
            q_shape = data.shape
            q_chunks = (data.chunks[0], (np.nan,))
            r_shape = (np.nan, np.nan)
            r_chunks = ((np.nan,), (np.nan,))
        elif is_unknown_m and not is_unknown_n:
            # assumption: m >= n
            q_shape = data.shape
            q_chunks = (data.chunks[0], (n,))
            r_shape = (n, n)
            r_chunks = (n, n)
        elif not is_unknown_m and is_unknown_n:
            # assumption: m >= n
            q_shape = data.shape
            q_chunks = (data.chunks[0], (np.nan,))
            r_shape = (np.nan, np.nan)
            r_chunks = ((np.nan,), (np.nan,))
        else:
            q_shape = data.shape if data.shape[0] >= data.shape[1] else (data.shape[0], data.shape[0])
            q_chunks = data.chunks if data.shape[0] >= data.shape[1] else (data.chunks[0], data.chunks[0])
            r_shape = (n, n) if data.shape[0] >= data.shape[1] else data.shape
            r_chunks = r_shape

        q = Array(dsk, name_q_st3,
                  shape=q_shape, chunks=q_chunks, dtype=qq.dtype)
        r = Array(dsk, name_r_st2,
                  shape=r_shape, chunks=r_chunks, dtype=rr.dtype)
        return q, r
    else:
        # In-core SVD computation
        name_svd_st2 = 'svd' + token + '-2'
        dsk_svd_st2 = top(np.linalg.svd, name_svd_st2, 'ij', name_r_st2, 'ij',
                          numblocks={name_r_st2: (1, 1)})
        # svd[0]
        name_u_st2 = 'getitem' + token + '-u2'
        dsk_u_st2 = {(name_u_st2, 0, 0): (operator.getitem,
                                          (name_svd_st2, 0, 0), 0)}
        # svd[1]
        name_s_st2 = 'getitem' + token + '-s2'
        dsk_s_st2 = {(name_s_st2, 0): (operator.getitem,
                                       (name_svd_st2, 0, 0), 1)}
        # svd[2]
        name_v_st2 = 'getitem' + token + '-v2'
        dsk_v_st2 = {(name_v_st2, 0, 0): (operator.getitem,
                                          (name_svd_st2, 0, 0), 2)}
        # Q * U
        name_u_st4 = 'getitem' + token + '-u4'
        dsk_u_st4 = top(dotmany, name_u_st4, 'ij', name_q_st3, 'ik',
                        name_u_st2, 'kj', numblocks={name_q_st3: numblocks,
                                                     name_u_st2: (1, 1)})

        dsk.update_with_key(dsk_svd_st2, key=name_svd_st2)
        dsk.update_with_key(dsk_u_st2, key=name_u_st2)
        dsk.update_with_key(dsk_u_st4, key=name_u_st4)
        dsk.update_with_key(dsk_s_st2, key=name_s_st2)
        dsk.update_with_key(dsk_v_st2, key=name_v_st2)

        uu, ss, vvh = np.linalg.svd(np.ones(shape=(1, 1), dtype=data.dtype))

        k = _nanmin(m, n)  # avoid RuntimeWarning with np.nanmin([m, n])

        m_u = m
        n_u = int(k) if not np.isnan(k) else k
        n_s = n_u
        m_vh = n_u
        n_vh = n
        d_vh = max(m_vh, n_vh)  # full matrix returned: but basically n
        u = Array(dsk, name_u_st4, shape=(m_u, n_u), chunks=(data.chunks[0], (n_u,)),
                  dtype=uu.dtype)
        s = Array(dsk, name_s_st2, shape=(n_s,), chunks=((n_s,),), dtype=ss.dtype)
        vh = Array(dsk, name_v_st2, shape=(d_vh, d_vh), chunks=((n,), (n,)),
                   dtype=vvh.dtype)
        return u, s, vh
