def linspace(start, stop, num=50, chunks=None, dtype=None):
    """
    Return `num` evenly spaced values over the closed interval [`start`,
    `stop`].

    TODO: implement the `endpoint`, `restep`, and `dtype` keyword args

    Parameters
    ----------
    start : scalar
        The starting value of the sequence.
    stop : scalar
        The last value of the sequence.
    num : int, optional
        Number of samples to include in the returned dask array, including the
        endpoints.
    chunks :  int
        The number of samples on each block. Note that the last block will have
        fewer samples if `num % blocksize != 0`

    Returns
    -------
    samples : dask array

    See Also
    --------
    dask.array.arange
    """
    num = int(num)

    if chunks is None:
        raise ValueError("Must supply a chunks= keyword argument")

    chunks = normalize_chunks(chunks, (num,))

    range_ = stop - start

    space = float(range_) / (num - 1)

    if dtype is None:
        dtype = np.linspace(0, 1, 1).dtype

    name = 'linspace-' + tokenize((start, stop, num, chunks, dtype))

    dsk = {}
    blockstart = start

    for i, bs in enumerate(chunks[0]):
        blockstop = blockstart + ((bs - 1) * space)
        task = (partial(np.linspace, dtype=dtype), blockstart, blockstop, bs)
        blockstart = blockstart + (space * bs)
        dsk[(name, i)] = task

    return Array(dsk, name, chunks, dtype=dtype)
