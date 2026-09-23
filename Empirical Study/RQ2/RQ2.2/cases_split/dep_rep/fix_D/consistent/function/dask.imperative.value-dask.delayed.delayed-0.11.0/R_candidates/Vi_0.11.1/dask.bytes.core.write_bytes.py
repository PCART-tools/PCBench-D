def write_bytes(data, urlpath, name_function=None, compression=None,
                encoding=None, **kwargs):
    """For a list of values which evaluate to byte, produce delayed values
    which, when executed, result in writing to files.

    The path maybe a concrete directory, in which case it is interpreted
    as a directory, or a template for numbered output.

    The path may be preceded by a protocol, like ``s3://`` or ``hdfs://`` if
    those libraries are installed.

    Parameters
    ----------
    data: list of ``dask.Delayed`` objects or dask collection
        the data to be written
    urlpath: string
        Absolute or relative filepaths, URLs (may include protocols like
        ``s3://``); may be globstring (include `*`).
    name_function: function or None
        If using a globstring, this provides the conversion from part number
        to test to replace `*` with.
    compression: string or None
        String like 'gzip' or 'xz'.  Must support efficient random access.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Examples
    --------
    >>> values = write_bytes(vals, 's3://bucket/part-*.csv')  # doctest: +SKIP

    Returns
    -------
    list of ``dask.Delayed`` objects
    """
    if isinstance(urlpath, (tuple, list, set)):
        if len(data) != len(urlpath):
            raise ValueError('Number of paths and number of delayed objects'
                             'must match (%s != %s)', len(urlpath), len(data))
        storage_options = infer_storage_options(urlpath[0],
                                                inherit_storage_options=kwargs)
        del storage_options['path']
        paths = [infer_storage_options(u, inherit_storage_options=kwargs)['path']
                 for u in urlpath]
    elif isinstance(urlpath, (str, unicode)):
        storage_options = infer_storage_options(urlpath,
                                                inherit_storage_options=kwargs)
        path = storage_options.pop('path')
        paths = _expand_paths(path, name_function, len(data))
    else:
        raise ValueError('URL spec must be string or sequence of strings')
    if compression == 'infer':
        compression = infer_compression(paths[0])
    if compression is not None and compression not in compress_files:
        raise ValueError("Compression type %s not supported" % compression)

    protocol = storage_options.pop('protocol')
    ensure_protocol(protocol)
    try:
        open_files_write = _open_files_write[protocol]
    except KeyError:
        raise NotImplementedError("Unknown protocol for writing %s (%s)" %
                                  (protocol, urlpath))

    keys = ['write-block-%s' % tokenize(d.key, p, storage_options,
            compression, encoding) for (d, p) in zip(data, paths)]
    return [Delayed(key, dasks=[{key: (write_block_to_file, v.key,
                                       (apply, open_files_write, (p,),
                                        storage_options),
                                       compression, encoding),
                                 }, v.dask])
            for key, v, p in zip(keys, data, paths)]
