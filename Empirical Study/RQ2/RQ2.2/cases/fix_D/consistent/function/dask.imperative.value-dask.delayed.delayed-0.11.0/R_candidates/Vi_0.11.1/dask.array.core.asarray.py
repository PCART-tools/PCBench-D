def asarray(array):
    """Coerce argument into a dask array

    >>> x = np.arange(3)
    >>> asarray(x)
    dask.array<asarray..., shape=(3,), dtype=int64, chunksize=(3,)>
    """
    if not isinstance(array, Array):
        name = 'asarray-' + tokenize(array)
        if isinstance(getattr(array, 'shape', None), Iterable):
            array = np.asarray(array)
        array = from_array(array, chunks=array.shape, name=name)
    return array
