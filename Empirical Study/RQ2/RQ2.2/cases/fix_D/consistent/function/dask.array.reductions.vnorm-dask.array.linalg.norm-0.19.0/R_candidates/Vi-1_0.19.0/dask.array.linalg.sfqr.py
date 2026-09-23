def sfqr(data, name=None):
    """ Direct Short-and-Fat QR

    Currently, this is a quick hack for non-tall-and-skinny matrices which
    are one chunk tall and (unless they are one chunk wide) have chunks
    that are wider than they are tall

    Q [R_1 R_2 ...] = [A_1 A_2 ...]

    it computes the factorization Q R_1 = A_1, then computes the other
    R_k's in parallel.

    Parameters
    ----------
    data: Array

    See Also
    --------
    dask.array.linalg.qr - Main user API that uses this function
    dask.array.linalg.tsqr - Variant for tall-and-skinny case
    """
    nr, nc = len(data.chunks[0]), len(data.chunks[1])
    cr, cc = data.chunks[0][0], data.chunks[1][0]

    if not ((data.ndim == 2) and  # Is a matrix
            (nr == 1) and         # Has exactly one block row
            ((cr <= cc) or        # Chunking dimension on rows is at least that on cols or...
             (nc == 1))):         # ... only one block col
        raise ValueError(
            "Input must have the following properties:\n"
            "  1. Have two dimensions\n"
            "  2. Have only one row of blocks\n"
            "  3. Either one column of blocks or (first) chunk size on cols\n"
            "     is at most that on rows (e.g.: for a 5x20 matrix,\n"
            "     chunks=((5), (8,4,8)) is fine, but chunks=((5), (4,8,8)) is not;\n"
            "     still, prefer something simple like chunks=(5,10) or chunks=5)\n\n"
            "Note: This function (sfqr) supports QR decomposition in the case\n"
            "of short-and-fat matrices (single row chunk/block; see qr)"
        )

    prefix = name or 'sfqr-' + tokenize(data)
    prefix += '_'

    m, n = data.shape

    qq, rr = np.linalg.qr(np.ones(shape=(1, 1), dtype=data.dtype))

    dsk = sharedict.ShareDict()
    dsk.update(data.dask)

    # data = A = [A_1 A_rest]
    name_A_1 = prefix + 'A_1'
    name_A_rest = prefix + 'A_rest'
    dsk.update_with_key({
        (name_A_1, 0, 0): (data.name, 0, 0)
    }, key=name_A_1)
    dsk.update_with_key({
        (name_A_rest, 0, idx): (data.name, 0, 1 + idx)
        for idx in range(nc - 1)
    }, key=name_A_rest)

    # Q R_1 = A_1
    name_Q_R1 = prefix + 'Q_R_1'
    name_Q = prefix + 'Q'
    name_R_1 = prefix + 'R_1'
    dsk.update_with_key({
        (name_Q_R1, 0, 0): (np.linalg.qr, (name_A_1, 0, 0))
    }, key=name_Q_R1)
    dsk.update_with_key({
        (name_Q, 0, 0): (operator.getitem, (name_Q_R1, 0, 0), 0)
    }, key=name_Q)
    dsk.update_with_key({
        (name_R_1, 0, 0): (operator.getitem, (name_Q_R1, 0, 0), 1),
    }, key=name_R_1)

    Q = Array(dsk, name_Q,
              shape=(m, min(m, n)), chunks=(m, min(m, n)), dtype=qq.dtype)
    R_1 = Array(dsk, name_R_1,
                shape=(min(m, n), cc), chunks=(cr, cc), dtype=rr.dtype)

    # R = [R_1 Q'A_rest]
    Rs = [R_1]

    if nc > 1:
        A_rest = Array(dsk, name_A_rest,
                       shape=(min(m, n), n - cc), chunks=((cr), data.chunks[1][1:]), dtype=rr.dtype)
        Rs.append(Q.T.dot(A_rest))

    R = concatenate(Rs, axis=1)

    return Q, R
