def write_bytes(data, urlpath, name_function=None, compression=None,
                encoding=None, **kwargs):
    """Write dask data to a set of files

    Parameters
    ----------
    data: list of delayed objects
        Producing data to write
    urlpath: list or template
        Location(s) to write to, including backend specifier.
    name_function: function or None
        If urlpath is a template, use this function to create a string out
        of the sequence number.
    compression: str or None
        Compression algorithm to apply (e.g., gzip), if any
    encoding: str or None
        If None, data must produce bytes, else will be encoded.
    kwargs: passed to filesystem constructor
    """
    mode = 'wb' if encoding is None else 'wt'
    fs, names, myopen = get_fs_paths_myopen(urlpath, compression, mode,
                                            name_function=name_function,
                                            num=len(data), encoding=encoding,
                                            **kwargs)

    return [delayed(write_block_to_file, pure=False)(d, myopen(f, mode='wb'))
            for d, f in zip(data, names)]
