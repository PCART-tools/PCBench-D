def linspace(start, stop, num=50, endpoint=True, retstep=False, chunks=None,
             dtype=None):
    """
    Return `num` evenly spaced values over the closed interval [`start`,
    `stop`].

    Parameters
    ----------
    start : scalar
        The starting value of the sequence.
    stop : scalar
        The last value of the sequence.
    num : int, optional
        Number of samples to include in the returned dask array, including the
        endpoints. Default is 50.
    endpoint : bool, optional
        If True, ``stop`` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (samples, step), where step is the spacing between
        samples. Default is False.
    chunks :  int
        The number of samples on each block. Note that the last block will have
        fewer samples if `num % blocksize != 0`
    dtype : dtype, optional
        The type of the output array. Default is given by ``numpy.dtype(float)``.

    Returns
    -------
    samples : dask array
    step : float, optional
        Only returned if ``retstep`` is True. Size of spacing between samples.


    See Also
    --------
    dask.array.arange
    """
    num = int(num)

    if chunks is None:
        raise ValueError("Must supply a chunks= keyword argument")

    chunks = normalize_chunks(chunks, (num,))

    range_ = stop - start

    div = (num - 1) if endpoint else num
    step = float(range_) / div

    if dtype is None:
        dtype = np.linspace(0, 1, 1).dtype

    name = 'linspace-' + tokenize((start, stop, num, endpoint, chunks, dtype))

    dsk = {}
    blockstart = start

    for i, bs in enumerate(chunks[0]):
        bs_space = bs - 1 if endpoint else bs
        blockstop = blockstart + (bs_space * step)
        task = (partial(np.linspace, endpoint=endpoint, dtype=dtype),
                blockstart, blockstop, bs)
        blockstart = blockstart + (step * bs)
        dsk[(name, i)] = task

    if retstep:
        return Array(dsk, name, chunks, dtype=dtype), step
    else:
        return Array(dsk, name, chunks, dtype=dtype)
