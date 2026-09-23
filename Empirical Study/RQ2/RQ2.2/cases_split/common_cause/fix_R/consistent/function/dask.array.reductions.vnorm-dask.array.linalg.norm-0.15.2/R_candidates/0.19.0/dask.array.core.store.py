def store(sources, targets, lock=True, regions=None, compute=True,
          return_stored=False, **kwargs):
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
    targets: array-like or Delayed or iterable of array-likes and/or Delayeds
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
    return_stored: boolean, optional
        Optionally return the stored result (default False).

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

    # Optimize all sources together
    sources_dsk = sharedict.merge(*[e.__dask_graph__() for e in sources])
    sources_dsk = Array.__dask_optimize__(
        sources_dsk,
        list(core.flatten([e.__dask_keys__() for e in sources]))
    )
    sources2 = [Array(sources_dsk, e.name, e.chunks, e.dtype) for e in sources]

    # Optimize all targets together
    targets2 = []
    targets_keys = []
    targets_dsk = []
    for e in targets:
        if isinstance(e, Delayed):
            targets2.append(e.key)
            targets_keys.extend(e.__dask_keys__())
            targets_dsk.append(e.__dask_graph__())
        elif is_dask_collection(e):
            raise TypeError(
                "Targets must be either Delayed objects or array-likes"
            )
        else:
            targets2.append(e)

    targets_dsk = sharedict.merge(*targets_dsk)
    targets_dsk = Delayed.__dask_optimize__(targets_dsk, targets_keys)

    load_stored = (return_stored and not compute)
    toks = [str(uuid.uuid1()) for _ in range(len(sources))]
    store_dsk = sharedict.merge(*[
        insert_to_ooc(s, t, lock, r, return_stored, load_stored, tok)
        for s, t, r, tok in zip(sources2, targets2, regions, toks)
    ])
    store_keys = list(store_dsk.keys())

    store_dsk = sharedict.merge(store_dsk, targets_dsk, sources_dsk)

    if return_stored:
        load_store_dsk = store_dsk
        if compute:
            store_dlyds = [Delayed(k, store_dsk) for k in store_keys]
            store_dlyds = persist(*store_dlyds, **kwargs)
            store_dsk_2 = sharedict.merge(*[e.dask for e in store_dlyds])

            load_store_dsk = retrieve_from_ooc(
                store_keys, store_dsk, store_dsk_2
            )

        result = tuple(
            Array(load_store_dsk, 'load-store-%s' % t, s.chunks, s.dtype)
            for s, t in zip(sources, toks)
        )

        return result
    else:
        name = 'store-' + str(uuid.uuid1())
        dsk = sharedict.merge({name: store_keys}, store_dsk)
        result = Delayed(name, dsk)

        if compute:
            result.compute(**kwargs)
            return None
        else:
            return result
