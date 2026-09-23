def read_bytes(urlpath, delimiter=None, not_zero=False, blocksize=2**27,
               sample=True, compression=None, **kwargs):
    """ Convert path to a list of delayed values

    The path may be a filename like ``'2015-01-01.csv'`` or a globstring
    like ``'2015-*-*.csv'``.

    The path may be preceded by a protocol, like ``s3://`` or ``hdfs://`` if
    those libraries are installed.

    This cleanly breaks data by a delimiter if given, so that block boundaries
    start directly after a delimiter and end on the delimiter.

    Parameters
    ----------
    urlpath: string
        Absolute or relative filepath, URL (may include protocols like
        ``s3://``), or globstring pointing to data.
    delimiter: bytes
        An optional delimiter, like ``b'\\n'`` on which to split blocks of
        bytes.
    not_zero: bool
        Force seek of start-of-file delimiter, discarding header.
    blocksize: int (=128MB)
        Chunk size
    compression: string or None
        String like 'gzip' or 'xz'.  Must support efficient random access.
    sample: bool or int
        Whether or not to return a header sample. If an integer is given it is
        used as sample size, otherwise the default sample size is 10kB.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Examples
    --------
    >>> sample, blocks = read_bytes('2015-*-*.csv', delimiter=b'\\n')  # doctest: +SKIP
    >>> sample, blocks = read_bytes('s3://bucket/2015-*-*.csv', delimiter=b'\\n')  # doctest: +SKIP

    Returns
    -------
    A sample header and list of ``dask.Delayed`` objects or list of lists of
    delayed objects if ``fn`` is a globstring.
    """
    fs, paths, myopen = get_fs_paths_myopen(urlpath, compression, 'rb',
                                            None, **kwargs)
    client = None
    if len(paths) == 0:
        raise IOError("%s resolved to no files" % urlpath)

    blocks, lengths, machines = fs.get_block_locations(paths)
    if blocks:
        offsets = blocks
    elif blocksize is None:
        offsets = [[0]] * len(paths)
        lengths = [[None]] * len(offsets)
        machines = [[None]] * len(offsets)
    else:
        offsets = []
        lengths = []
        for path in paths:
            try:
                size = fs.logical_size(path, compression)
            except KeyError:
                raise ValueError('Cannot read compressed files (%s) in byte chunks,'
                                 'use blocksize=None' % infer_compression(urlpath))
            off = list(range(0, size, blocksize))
            length = [blocksize] * len(off)
            if not_zero:
                off[0] = 1
                length[0] -= 1
            offsets.append(off)
            lengths.append(length)
        machines = [[None]] * len(offsets)

    out = []
    for path, offset, length, machine in zip(paths, offsets, lengths, machines):
        ukey = fs.ukey(path)
        keys = ['read-block-%s-%s' %
                (o, tokenize(path, compression, offset, ukey, kwargs, delimiter))
                for o in offset]
        L = [delayed(read_block_from_file)(myopen(path, mode='rb'), o,
                                           l, delimiter, dask_key_name=key)
             for (o, key, l) in zip(offset, keys, length)]
        out.append(L)
        if machine is not None:  # blocks are in preferred locations
            if client is None:
                try:
                    from distributed.client import default_client
                    client = default_client()
                except (ImportError, ValueError):  # no distributed client
                    client = False
            if client:
                restrictions = {key: w for key, w in zip(keys, machine)}
                client._send_to_scheduler({'op': 'update-graph', 'tasks': {},
                                           'dependencies': [], 'keys': [],
                                           'restrictions': restrictions,
                                           'loose_restrictions': list(restrictions),
                                           'client': client.id})

    if sample is not True:
        nbytes = sample
    else:
        nbytes = 10000
    if sample:
        # myopen = OpenFileCreator(urlpath, compression)
        with myopen(paths[0], 'rb') as f:
            sample = read_block(f, 0, nbytes, delimiter)
    return sample, out
