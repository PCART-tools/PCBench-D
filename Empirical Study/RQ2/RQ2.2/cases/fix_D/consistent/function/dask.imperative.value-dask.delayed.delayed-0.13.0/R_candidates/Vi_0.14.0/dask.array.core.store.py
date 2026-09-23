def store(sources, targets, lock=True, regions=None, compute=True, **kwargs):
    """ Store dask arrays in array-like objects, overwrite data in target

    This stores dask arrays into object that supports numpy-style setitem
    indexing.  It stores values chunk by chunk so that it does not have to
    fill up memory.  For best performance you can align the block size of
    the storage target with the block size of your array.

    If your data fits in memory then you may prefer calling
    ``np.array(myarray)`` instead.

    Parameters
    ----------

    sources: Array or iterable of Arrays
    targets: array-like or iterable of array-likes
        These should support setitem syntax ``target[10:20] = ...``
    lock: boolean or threading.Lock, optional
        Whether or not to lock the data stores while storing.
        Pass True (lock each file individually), False (don't lock) or a
        particular ``threading.Lock`` object to be shared among all writes.
    regions: tuple of slices or iterable of tuple of slices
        Each ``region`` tuple in ``regions`` should be such that
        ``target[region].shape = source.shape``
        for the corresponding source and target in sources and targets, respectively.
    compute: boolean, optional
        If true compute immediately, return ``dask.delayed.Delayed`` otherwise

    Examples
    --------
    >>> x = ...  # doctest: +SKIP

    >>> import h5py  # doctest: +SKIP
    >>> f = h5py.File('myfile.hdf5')  # doctest: +SKIP
    >>> dset = f.create_dataset('/data', shape=x.shape,
    ...                                  chunks=x.chunks,
    ...                                  dtype='f8')  # doctest: +SKIP

    >>> store(x, dset)  # doctest: +SKIP

    Alternatively store many arrays at the same time

    >>> store([x, y, z], [dset1, dset2, dset3])  # doctest: +SKIP
    """
    if isinstance(sources, Array):
        sources = [sources]
        targets = [targets]

    if any(not isinstance(s, Array) for s in sources):
        raise ValueError("All sources must be dask array objects")

    if len(sources) != len(targets):
        raise ValueError("Different number of sources [%d] and targets [%d]"
                         % (len(sources), len(targets)))

    if isinstance(regions, tuple) or regions is None:
        regions = [regions]

    if len(sources) > 1 and len(regions) == 1:
        regions *= len(sources)

    if len(sources) != len(regions):
        raise ValueError("Different number of sources [%d] and targets [%d] than regions [%d]"
                         % (len(sources), len(targets), len(regions)))

    updates = [insert_to_ooc(tgt, src, lock=lock, region=reg)
               for tgt, src, reg in zip(targets, sources, regions)]
    keys = [key for u in updates for key in u]
    name = 'store-' + tokenize(*keys)
    dsk = sharedict.merge((name, toolz.merge(updates)), *[src.dask for src in sources])
    if compute:
        Array._get(dsk, keys, **kwargs)
    else:
        from ..delayed import Delayed
        dsk.update({name: keys})
        return Delayed(name, dict(dsk))
