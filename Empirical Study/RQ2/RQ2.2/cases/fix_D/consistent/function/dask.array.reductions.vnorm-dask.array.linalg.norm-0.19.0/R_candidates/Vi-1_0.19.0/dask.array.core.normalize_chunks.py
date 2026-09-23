def normalize_chunks(chunks, shape=None, limit=None, dtype=None,
                     previous_chunks=None):
    """ Normalize chunks to tuple of tuples

    This takes in a variety of input types and information and produces a full
    tuple-of-tuples result for chunks, suitable to be passed to Array or
    rechunk or any other operation that creates a Dask array.

    Parameters
    ----------
    chunks: tuple, int, dict, or string
        The chunks to be normalized.  See examples below for more details
    shape: Tuple[int]
        The shape of the array
    limit: int (optional)
        The maximum block size to target in bytes,
        if freedom is given to choose
    dtype: np.dtype
    previous_chunks: Tuple[Tuple[int]] optional
        Chunks from a previous array that we should use for inspiration when
        rechunking auto dimensions.  If not provided but auto-chunking exists
        then auto-dimensions will prefer square-like chunk shapes.

    Examples
    --------
    Specify uniform chunk sizes

    >>> normalize_chunks((2, 2), shape=(5, 6))
    ((2, 2, 1), (2, 2, 2))

    Also passes through fully explicit tuple-of-tuples

    >>> normalize_chunks(((2, 2, 1), (2, 2, 2)), shape=(5, 6))
    ((2, 2, 1), (2, 2, 2))

    Cleans up lists to tuples

    >>> normalize_chunks([[2, 2], [3, 3]])
    ((2, 2), (3, 3))

    Expands integer inputs 10 -> (10, 10)

    >>> normalize_chunks(10, shape=(30, 5))
    ((10, 10, 10), (5,))

    Expands dict inputs

    >>> normalize_chunks({0: 2, 1: 3}, shape=(6, 6))
    ((2, 2, 2), (3, 3))

    The value -1 gets mapped to full size

    >>> normalize_chunks((5, -1), shape=(10, 10))
    ((5, 5), (10,))

    Use the value "auto" to automatically determine chunk sizes along certain
    dimensions.  This uses the ``limit=`` and ``dtype=`` keywords to
    determine how large to make the chunks.  The term "auto" can be used
    anywhere an integer can be used.  See array chunking documentation for more
    information.

    >>> normalize_chunks(("auto",), shape=(20,), limit=5, dtype='uint8')
    ((5, 5, 5, 5),)

    Respects null dimensions

    >>> normalize_chunks((), shape=(0, 0))
    ((0,), (0,))
    """
    if dtype and not isinstance(dtype, np.dtype):
        dtype = np.dtype(dtype)
    if chunks is None:
        raise ValueError(CHUNKS_NONE_ERROR_MESSAGE)
    if isinstance(chunks, list):
        chunks = tuple(chunks)
    if isinstance(chunks, (Number, str)):
        chunks = (chunks,) * len(shape)
    if isinstance(chunks, dict):
        chunks = tuple(chunks.get(i, None) for i in range(len(shape)))
    if isinstance(chunks, np.ndarray):
        chunks = chunks.tolist()
    if not chunks and shape and all(s == 0 for s in shape):
        chunks = ((0,),) * len(shape)

    if (shape and len(shape) == 1 and len(chunks) > 1 and
            all(isinstance(c, (Number, str)) for c in chunks)):
        chunks = chunks,

    if shape and len(chunks) != len(shape):
        raise ValueError(
            "Chunks and shape must be of the same length/dimension. "
            "Got chunks=%s, shape=%s" % (chunks, shape))
    if -1 in chunks:
        chunks = tuple(s if c == -1 else c for c, s in zip(chunks, shape))

    if any(c == 'auto' for c in chunks):
        chunks = auto_chunks(chunks, shape, limit, dtype, previous_chunks)

    if shape is not None:
        chunks = tuple(c if c not in {None, -1} else s
                       for c, s in zip(chunks, shape))

    if chunks and shape is not None:
        chunks = sum((blockdims_from_blockshape((s,), (c,))
                      if not isinstance(c, (tuple, list)) else (c,)
                      for s, c in zip(shape, chunks)), ())
    for c in chunks:
        if not c:
            raise ValueError("Empty tuples are not allowed in chunks. Express "
                             "zero length dimensions with 0(s) in chunks")

    if shape is not None:
        if len(chunks) != len(shape):
            raise ValueError("Input array has %d dimensions but the supplied "
                             "chunks has only %d dimensions" %
                             (len(shape), len(chunks)))
        if not all(c == s or (math.isnan(c) or math.isnan(s))
                   for c, s in zip(map(sum, chunks), shape)):
            raise ValueError("Chunks do not add up to shape. "
                             "Got chunks=%s, shape=%s" % (chunks, shape))

    return tuple(tuple(int(x) if not math.isnan(x) else x for x in c) for c in chunks)
