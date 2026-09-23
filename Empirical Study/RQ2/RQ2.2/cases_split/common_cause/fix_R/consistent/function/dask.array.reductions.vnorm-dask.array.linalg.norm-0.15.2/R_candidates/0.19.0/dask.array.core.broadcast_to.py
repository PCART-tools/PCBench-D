def broadcast_to(x, shape, chunks=None):
    """Broadcast an array to a new shape.

    Parameters
    ----------
    x : array_like
        The array to broadcast.
    shape : tuple
        The shape of the desired array.
    chunks : tuple, optional
        If provided, then the result will use these chunks instead of the same
        chunks as the source array. Setting chunks explicitly as part of
        broadcast_to is more efficient than rechunking afterwards. Chunks are
        only allowed to differ from the original shape along dimensions that
        are new on the result or have size 1 the input array.

    Returns
    -------
    broadcast : dask array

    See Also
    --------
    :func:`numpy.broadcast_to`
    """
    x = asarray(x)
    shape = tuple(shape)

    if x.shape == shape and (chunks is None or chunks == x.chunks):
        return x

    ndim_new = len(shape) - x.ndim
    if ndim_new < 0 or any(new != old
                           for new, old in zip(shape[ndim_new:], x.shape)
                           if old != 1):
        raise ValueError('cannot broadcast shape %s to shape %s'
                         % (x.shape, shape))

    if chunks is None:
        chunks = (tuple((s,) for s in shape[:ndim_new]) +
                  tuple(bd if old > 1 else (new,)
                  for bd, old, new in zip(x.chunks, x.shape, shape[ndim_new:])))
    else:
        chunks = normalize_chunks(chunks, shape, dtype=x.dtype,
                                  previous_chunks=x.chunks)
        for old_bd, new_bd in zip(x.chunks, chunks[ndim_new:]):
            if old_bd != new_bd and old_bd != (1,):
                raise ValueError('cannot broadcast chunks %s to chunks %s: '
                                 'new chunks must either be along a new '
                                 'dimension or a dimension of size 1'
                                 % (x.chunks, chunks))

    name = 'broadcast_to-' + tokenize(x, shape, chunks)
    dsk = {}

    enumerated_chunks = product(*(enumerate(bds) for bds in chunks))
    for new_index, chunk_shape in (zip(*ec) for ec in enumerated_chunks):
        old_index = tuple(0 if bd == (1,) else i
                          for bd, i in zip(x.chunks, new_index[ndim_new:]))
        old_key = (x.name,) + old_index
        new_key = (name,) + new_index
        dsk[new_key] = (chunk.broadcast_to, old_key, quote(chunk_shape))

    return Array(sharedict.merge((name, dsk), x.dask), name, chunks,
                 dtype=x.dtype)
