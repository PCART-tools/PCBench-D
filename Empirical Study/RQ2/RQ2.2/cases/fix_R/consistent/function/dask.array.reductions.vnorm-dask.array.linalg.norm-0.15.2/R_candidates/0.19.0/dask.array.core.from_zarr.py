def from_zarr(url, component=None, storage_options=None, chunks=None, **kwargs):
    """Load array from the zarr storage format

    See https://zarr.readthedocs.io for details about the format.

    Parameters
    ----------
    url: Zarr Array or str or MutableMapping
        Location of the data. A URL can include a protocol specifier like s3://
        for remote data. Can also be any MutableMapping instance, which should
        be serializable if used in multiple processes.
    component: str or None
        If the location is a zarr group rather than an array, this is the
        subcomponent that should be loaded, something like ``'foo/bar'``.
    storage_options: dict
        Any additional parameters for the storage backend (ignored for local
        paths)
    chunks: tuple of ints or tuples of ints
        Passed to ``da.from_array``, allows setting the chunks on
        initialisation, if the chunking scheme in the on-disc dataset is not
        optimal for the calculations to follow.
    kwargs: passed to ``zarr.Array``.
    """
    import zarr
    storage_options = storage_options or {}
    if isinstance(url, zarr.Array):
        z = url
    elif isinstance(url, str):
        fs, fs_token, path = get_fs_token_paths(
            url, 'rb', storage_options=storage_options)
        assert len(path) == 1
        mapper = get_mapper(fs, path[0])
        z = zarr.Array(mapper, read_only=True, path=component, **kwargs)
    else:
        mapper = url
        z = zarr.Array(mapper, read_only=True, path=component, **kwargs)
    chunks = chunks if chunks is not None else z.chunks
    return from_array(z, chunks, name='zarr-%s' % url)
