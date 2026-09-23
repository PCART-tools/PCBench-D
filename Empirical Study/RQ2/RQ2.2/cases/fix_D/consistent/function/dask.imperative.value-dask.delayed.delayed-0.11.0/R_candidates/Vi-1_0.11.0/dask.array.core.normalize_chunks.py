def normalize_chunks(chunks, shape=None):
    """ Normalize chunks to tuple of tuples

    >>> normalize_chunks((2, 2), shape=(5, 6))
    ((2, 2, 1), (2, 2, 2))

    >>> normalize_chunks(((2, 2, 1), (2, 2, 2)), shape=(4, 6))  # Idempotent
    ((2, 2, 1), (2, 2, 2))

    >>> normalize_chunks([[2, 2], [3, 3]])  # Cleans up lists to tuples
    ((2, 2), (3, 3))

    >>> normalize_chunks(10, shape=(30, 5))  # Supports integer inputs
    ((10, 10, 10), (5,))

    >>> normalize_chunks((), shape=(0, 0))  #  respects null dimensions
    ((), ())
    """
    if chunks is None:
        raise ValueError(chunks_none_error_message)
    if isinstance(chunks, list):
        chunks = tuple(chunks)
    if isinstance(chunks, Number):
        chunks = (chunks,) * len(shape)
    if not chunks and shape and all(s == 0 for s in shape):
        chunks = ((),) * len(shape)

    if shape is not None:
        chunks = tuple(c if c is not None else s for c, s in zip(chunks, shape))

    if chunks and shape is not None:
        chunks = sum((blockdims_from_blockshape((s,), (c,))
                      if not isinstance(c, (tuple, list)) else (c,)
                      for s, c in zip(shape, chunks)), ())

    return tuple(map(tuple, chunks))
