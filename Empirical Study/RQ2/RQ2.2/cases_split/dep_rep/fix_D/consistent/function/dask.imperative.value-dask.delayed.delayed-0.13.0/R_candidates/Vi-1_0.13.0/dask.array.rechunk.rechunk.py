def rechunk(x, chunks, threshold=DEFAULT_THRESHOLD,
            block_size_limit=DEFAULT_BLOCK_SIZE_LIMIT):
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
    chunks:  tuple
        The new block dimensions to create
    threshold: int
        The graph growth factor under which we don't bother
        introducing an intermediate step
    block_size_limit: int
        The maximum block size (in bytes) we want to produce during an
        intermediate step
    """
    threshold = threshold or DEFAULT_THRESHOLD
    block_size_limit = block_size_limit or DEFAULT_BLOCK_SIZE_LIMIT

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

    steps = plan_rechunk(x.chunks, chunks, x.dtype.itemsize,
                         threshold, block_size_limit)
    for c in steps:
        x = _compute_rechunk(x, c)

    return x
