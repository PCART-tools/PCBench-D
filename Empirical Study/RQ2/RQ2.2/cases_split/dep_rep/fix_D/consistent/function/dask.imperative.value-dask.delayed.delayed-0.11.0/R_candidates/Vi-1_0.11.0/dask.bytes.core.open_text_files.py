def open_text_files(urlpath, encoding=system_encoding, errors='strict',
        compression=None, **kwargs):
    """ Given path return dask.delayed file-like objects in text mode

    Parameters
    ----------
    urlpath: string
        Absolute or relative filepath, URL (may include protocols like
        ``s3://``), or globstring pointing to data.
    encoding: string
    errors: string
    compression: string
        Compression to use.  See ``dask.bytes.compression.files`` for options.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Examples
    --------
    >>> files = open_text_files('2015-*-*.csv', encoding='utf-8')  # doctest: +SKIP
    >>> files = open_text_files('s3://bucket/2015-*-*.csv')  # doctest: +SKIP

    Returns
    -------
    List of ``dask.delayed`` objects that compute to text file-like objects
    """
    if compression is not None and compression not in compress_files:
        raise ValueError("Compression type %s not supported" % compression)

    storage_options = infer_storage_options(urlpath,
                                            inherit_storage_options=kwargs)
    path = storage_options.pop('path')
    protocol = storage_options.pop('protocol')
    ensure_protocol(protocol)
    if protocol in _open_text_files and compression is None:
        return _open_text_files[protocol](path,
                                          encoding=encoding,
                                          errors=errors,
                                          **storage_options)
    elif protocol in _open_files:
        files = open_files_by(_open_files[protocol],
                              path,
                              compression=compression,
                              **storage_options)
        if PY2:
            files = [delayed(SeekableFile)(file) for file in files]
        return [delayed(io.TextIOWrapper)(file, encoding=encoding,
                                          errors=errors) for file in files]
    else:
        raise NotImplementedError("Unknown protocol %s (%s)" %
                                  (protocol, urlpath))
