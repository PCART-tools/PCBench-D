def rechunk(x, chunks):
    """
    Convert blocks in dask array x for new chunks.

    >>> import dask.array as da
    >>> a = np.random.uniform(0, 1, 7**4).reshape((7,) * 4)
    >>> x = da.from_array(a, chunks=((2, 3, 2),)*4)
    >>> x.chunks
    ((2, 3, 2), (2, 3, 2), (2, 3, 2), (2, 3, 2))

    >>> y = rechunk(x, chunks=((2, 4, 1), (4, 2, 1), (4, 3), (7,)))
    >>> y.chunks
    ((2, 4, 1), (4, 2, 1), (4, 3), (7,))

    chunks also accept dict arguments mapping axis to blockshape

    >>> y = rechunk(x, chunks={1: 2})  # rechunk axis 1 with blockshape 2

    Parameters
    ----------

    x:   dask array
    chunks:  the new block dimensions to create
    """
    if isinstance(chunks, dict):
        if not chunks or isinstance(next(iter(chunks.values())), int):
            chunks = blockshape_dict_to_tuple(x.chunks, chunks)
        else:
            chunks = blockdims_dict_to_tuple(x.chunks, chunks)
    if isinstance(chunks, (tuple, list)):
        chunks = tuple(lc if lc is not None else rc
                       for lc, rc in zip(chunks, x.chunks))
    chunks = normalize_chunks(chunks, x.shape)
    if chunks == x.chunks:
        return x
    ndim = x.ndim
    if not len(chunks) == ndim or tuple(map(sum, chunks)) != x.shape:
        raise ValueError("Provided chunks are not consistent with shape")

    crossed = intersect_chunks(x.chunks, chunks)
    x2 = dict()
    intermediates = dict()
    token = tokenize(x, chunks)
    temp_name = 'rechunk-merge-' + token
    new_index = tuple(product(*(tuple(range(len(n))) for n in chunks)))
    for flat_idx, cross1 in enumerate(crossed):
        new_idx = new_index[flat_idx]
        key = (temp_name,) + new_idx
        cr2 = iter(cross1)
        old_blocks = [[ind for ind, _ in cr] for cr in cross1]
        subdims = [len(set([ss[i] for ss in old_blocks])) for i in range(ndim)]
        rec_cat_arg = np.empty(subdims).tolist()
        inds_in_block = product(*[range(s) for s in subdims])
        for old_block in old_blocks:
            ind_slics = next(cr2)
            old_inds = [[s[0] for s in ind_slics] for i in range(ndim)]
            # list of nd slices
            slic = [[s[1] for s in ind_slics] for i in range(ndim)]
            ind_in_blk = next(inds_in_block)
            temp = rec_cat_arg
            for i in range(ndim - 1):
                temp = getitem(temp, ind_in_blk[i])
            for ind, slc in zip(old_inds, slic):
                name = (('rechunk-split-' + token,)
                        + tuple(ind)
                        + sum([(s.start, s.stop) for s in slc], ()))
                intermediates[name] = (getitem, (x.name,) + tuple(ind),
                                                 tuple(slc))
                temp[ind_in_blk[-1]] = name
        x2[key] = (concatenate3, rec_cat_arg)
    x2 = merge(x.dask, x2, intermediates)
    return Array(x2, temp_name, chunks, dtype=x.dtype)
