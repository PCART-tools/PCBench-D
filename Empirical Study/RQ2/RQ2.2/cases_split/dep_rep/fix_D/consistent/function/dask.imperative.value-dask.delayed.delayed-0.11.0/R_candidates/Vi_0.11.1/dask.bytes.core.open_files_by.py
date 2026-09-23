def open_files_by(open_files_backend, path, compression=None, **kwargs):
    """ Given open files backend and path return dask.delayed file-like objects

    NOTE: This is an internal helper function, please refer to
    :func:`open_files` documentation for more details.

    Parameters
    ----------
    path: string
        Filepath or globstring
    compression: string
        Compression to use.  See ``dask.bytes.compression.files`` for options.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Returns
    -------
    List of ``dask.delayed`` objects that compute to file-like objects
    """
    files = open_files_backend(path, **kwargs)

    if compression:
        decompress = merge(seekable_files, compress_files)[compression]
        if PY2:
            files = [delayed(SeekableFile)(file) for file in files]
        files = [delayed(decompress)(file) for file in files]

    return files
