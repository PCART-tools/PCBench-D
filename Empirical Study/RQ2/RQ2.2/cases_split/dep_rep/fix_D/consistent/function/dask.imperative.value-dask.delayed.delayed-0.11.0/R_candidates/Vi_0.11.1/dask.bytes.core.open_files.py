def open_files(urlpath, compression=None, **kwargs):
    """ Given path return dask.delayed file-like objects

    Parameters
    ----------
    urlpath: string
        Absolute or relative filepath, URL (may include protocols like
        ``s3://``), or globstring pointing to data.
    compression: string
        Compression to use.  See ``dask.bytes.compression.files`` for options.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Examples
    --------
    >>> files = open_files('2015-*-*.csv')  # doctest: +SKIP
    >>> files = open_files('s3://bucket/2015-*-*.csv.gz', compression='gzip')  # doctest: +SKIP

    Returns
    -------
    List of ``dask.delayed`` objects that compute to file-like objects
    """
    if compression is not None and compression not in compress_files:
        raise ValueError("Compression type %s not supported" % compression)

    storage_options = infer_storage_options(urlpath,
                                            inherit_storage_options=kwargs)
    protocol = storage_options.pop('protocol')
    ensure_protocol(protocol)
    try:
        open_files_backend = _open_files[protocol]
    except KeyError:
        raise NotImplementedError("Unknown protocol %s (%s)" %
                                  (protocol, urlpath))

    return open_files_by(open_files_backend, storage_options.pop('path'),
                         compression=compression, **storage_options)
