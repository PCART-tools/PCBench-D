def reshape(x, shape):
    """ Reshape array to new shape

    This is a parallelized version of the ``np.reshape`` function with the
    following limitations:

    1.  It assumes that the array is stored in C-order
    2.  It only allows for reshapings that collapse or merge dimensions like
        ``(1, 2, 3, 4) -> (1, 6, 4)`` or ``(64,) -> (4, 4, 4)``

    When communication is necessary this algorithm depends on the logic within
    rechunk.  It endeavors to keep chunk sizes roughly the same when possible.

    See Also
    --------
    dask.array.rechunk
    numpy.reshape
    """
    # Sanitize inputs, look for -1 in shape
    from .slicing import sanitize_index
    shape = tuple(map(sanitize_index, shape))
    known_sizes = [s for s in shape if s != -1]
    if len(known_sizes) < len(shape):
        if len(known_sizes) - len(shape) > 1:
            raise ValueError('can only specify one unknown dimension')
        missing_size = sanitize_index(x.size / reduce(mul, known_sizes, 1))
        shape = tuple(missing_size if s == -1 else s for s in shape)

    if np.isnan(sum(x.shape)):
        raise ValueError("Array chunk size or shape is unknown. shape: %s", x.shape)

    if reduce(mul, shape, 1) != x.size:
        raise ValueError('total size of new array must be unchanged')

    if x.shape == shape:
        return x

    name = 'reshape-' + tokenize(x, shape)

    if x.npartitions == 1:
        key = next(flatten(x.__dask_keys__()))
        dsk = {(name,) + (0,) * len(shape): (M.reshape, key, shape)}
        chunks = tuple((d,) for d in shape)
        return Array(sharedict.merge((name, dsk), x.dask), name, chunks,
                     dtype=x.dtype)

    # Logic for how to rechunk
    inchunks, outchunks = reshape_rechunk(x.shape, shape, x.chunks)
    x2 = x.rechunk(inchunks)

    # Construct graph
    in_keys = list(product([x2.name], *[range(len(c)) for c in inchunks]))
    out_keys = list(product([name], *[range(len(c)) for c in outchunks]))
    shapes = list(product(*outchunks))
    dsk = {a: (M.reshape, b, shape) for a, b, shape in zip(out_keys, in_keys, shapes)}

    return Array(sharedict.merge((name, dsk), x2.dask), name, outchunks,
                 dtype=x.dtype)
