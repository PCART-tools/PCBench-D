def rechunk(x, chunks, threshold=None, block_size_limit=None):
    """
    Convert blocks in dask array x for new chunks.

    Parameters
    ----------
    x: dask array
        Array to be rechunked.
    chunks:  int, tuple or dict
        The new block dimensions to create. -1 indicates the full size of the
        corresponding dimension.
    threshold: int
        The graph growth factor under which we don't bother introducing an
        intermediate step.
    block_size_limit: int
        The maximum block size (in bytes) we want to produce
        Defaults to the configuration value ``array.chunk-size``

    Examples
    --------
    >>> import dask.array as da
    >>> x = da.ones((1000, 1000), chunks=(100, 100))

    Specify uniform chunk sizes with a tuple

    >>> y = x.rechunk((1000, 10))

    Or chunk only specific dimensions with a dictionary

    >>> y = x.rechunk({0: 1000})

    Use the value ``-1`` to specify that you want a single chunk along a
    dimension or the value ``"auto"`` to specify that dask can freely rechunk a
    dimension to attain blocks of a uniform block size

    >>> y = x.rechunk({0: -1, 1: 'auto'}, block_size_limit=1e8)
    """
    if isinstance(chunks, dict):
        chunks = {validate_axis(c, x.ndim): v for c, v in chunks.items()}
        for i in range(x.ndim):
            if i not in chunks:
                chunks[i] = x.chunks[i]
    if isinstance(chunks, (tuple, list)):
        chunks = tuple(lc if lc is not None else rc
                       for lc, rc in zip(chunks, x.chunks))
    chunks = normalize_chunks(chunks, x.shape, limit=block_size_limit,
                              dtype=x.dtype, previous_chunks=x.chunks)

    if chunks == x.chunks:
        return x
    ndim = x.ndim
    if not len(chunks) == ndim:
        raise ValueError("Provided chunks are not consistent with shape")
    new_shapes = tuple(map(sum, chunks))

    for new, old in zip(new_shapes, x.shape):
        if new != old and not math.isnan(old) and not math.isnan(new):
            raise ValueError("Provided chunks are not consistent with shape")

    steps = plan_rechunk(x.chunks, chunks, x.dtype.itemsize,
                         threshold, block_size_limit)
    for c in steps:
        x = _compute_rechunk(x, c)

    return x
