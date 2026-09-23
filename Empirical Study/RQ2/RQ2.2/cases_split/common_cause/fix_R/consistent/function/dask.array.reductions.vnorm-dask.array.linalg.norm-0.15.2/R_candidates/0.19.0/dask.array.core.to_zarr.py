def to_zarr(arr, url, component=None, storage_options=None,
            overwrite=False, compute=True, return_stored=False, **kwargs):
    """Save array to the zarr storage format

    See https://zarr.readthedocs.io for details about the format.

    Parameters
    ----------
    arr: dask.array
        Data to store
    url: Zarr Array or str or MutableMapping
        Location of the data. A URL can include a protocol specifier like s3://
        for remote data. Can also be any MutableMapping instance, which should
        be serializable if used in multiple processes.
    component: str or None
        If the location is a zarr group rather than an array, this is the
        subcomponent that should be created/over-written.
    storage_options: dict
        Any additional parameters for the storage backend (ignored for local
        paths)
    overwrite: bool
        If given array already exists, overwrite=False will cause an error,
        where overwrite=True will replace the existing data.
    compute, return_stored: see ``store()``
    kwargs: passed to the ``zarr.create()`` function, e.g., compression options
    """
    import zarr

    if isinstance(url, zarr.Array):
        z = url
        if (isinstance(z.store, (dict, zarr.DictStore)) and
                'distributed' in config.get('scheduler', '')):
            raise RuntimeError('Cannot store into in memory Zarr Array using '
                               'the Distributed Scheduler.')
        arr = arr.rechunk(z.chunks)
        return arr.store(z, lock=False, compute=compute,
                         return_stored=return_stored)

    if not _check_regular_chunks(arr.chunks):
        raise ValueError('Attempt to save array to zarr with irregular '
                         'chunking, please call `arr.rechunk(...)` first.')

    storage_options = storage_options or {}

    if isinstance(url, str):
        fs, fs_token, path = get_fs_token_paths(
            url, 'rb', storage_options=storage_options)
        assert len(path) == 1
        mapper = get_mapper(fs, path[0])
    else:
        # assume the object passed is already a mapper
        mapper = url

    chunks = [c[0] for c in arr.chunks]
    z = zarr.create(shape=arr.shape, chunks=chunks, dtype=arr.dtype,
                    store=mapper, path=component, overwrite=overwrite, **kwargs)
    return arr.store(z, lock=False, compute=compute,
                     return_stored=return_stored)
