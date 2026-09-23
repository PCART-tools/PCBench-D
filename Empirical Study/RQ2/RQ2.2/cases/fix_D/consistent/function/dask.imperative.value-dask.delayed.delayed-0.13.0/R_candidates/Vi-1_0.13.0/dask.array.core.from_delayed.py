def from_delayed(value, shape, dtype, name=None):
    """ Create a dask array from a dask delayed value

    This routine is useful for constructing dask arrays in an ad-hoc fashion
    using dask delayed, particularly when combined with stack and concatenate.

    The dask array will consist of a single chunk.

    Examples
    --------
    >>> from dask import delayed
    >>> value = delayed(np.ones)(5)
    >>> array = from_delayed(value, (5,), float)
    >>> array
    dask.array<from-va..., shape=(5,), dtype=float64, chunksize=(5,)>
    >>> array.compute()
    array([ 1.,  1.,  1.,  1.,  1.])
    """
    name = name or 'from-value-' + tokenize(value, shape, dtype)
    dsk = {(name,) + (0,) * len(shape): value.key}
    dsk.update(value.dask)
    chunks = tuple((d,) for d in shape)
    return Array(dsk, name, chunks, dtype)
