def _check_regular_chunks(chunkset):
    """Check if the chunks are regular

    "Regular" in this context means that along every axis, the chunks all
    have the same size, except the last one, which may be smaller

    Parameters
    ----------
    chunkset: tuple of tuples of ints
        From the ``.chunks`` attribute of an ``Array``

    Returns
    -------
    True if chunkset passes, else False

    Examples
    --------
    >>> import dask.array as da
    >>> arr = da.zeros(10, chunks=(5, ))
    >>> _check_regular_chunks(arr.chunks)
    True

    >>> arr = da.zeros(10, chunks=((3, 3, 3, 1), ))
    >>> _check_regular_chunks(arr.chunks)
    True

    >>> arr = da.zeros(10, chunks=((3, 1, 3, 3), ))
    >>> _check_regular_chunks(arr.chunks)
    False
    """
    for chunks in chunkset:
        if len(chunks) == 1:
            continue
        if len(set(chunks[:-1])) > 1:
            return False
        if chunks[-1] > chunks[0]:
            return False
    return True
