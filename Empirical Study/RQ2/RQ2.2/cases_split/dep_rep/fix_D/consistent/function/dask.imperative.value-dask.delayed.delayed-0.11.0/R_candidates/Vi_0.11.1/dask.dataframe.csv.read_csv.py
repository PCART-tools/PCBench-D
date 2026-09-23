def read_csv(urlpath, blocksize=AUTO_BLOCKSIZE, collection=True,
             lineterminator=None, compression=None, sample=256000,
             enforce=False, storage_options=None, **kwargs):
    """ Read CSV files into a Dask.DataFrame

    This parallelizes the ``pandas.read_csv`` file in the following ways:

    1.  It supports loading many files at once using globstrings as follows:

        >>> df = dd.read_csv('myfiles.*.csv')  # doctest: +SKIP

    2.  In some cases it can break up large files as follows:

        >>> df = dd.read_csv('largefile.csv', blocksize=25e6)  # 25MB chunks  # doctest: +SKIP

    3.  You can read CSV files from external resources (e.g. S3, HDFS)
        providing a URL:

        >>> df = dd.read_csv('s3://bucket/myfiles.*.csv')  # doctest: +SKIP
        >>> df = dd.read_csv('hdfs:///myfiles.*.csv')  # doctest: +SKIP
        >>> df = dd.read_csv('hdfs://namenode.example.com/myfiles.*.csv')  # doctest: +SKIP

    Internally dd.read_csv uses pandas.read_csv and so supports many of the
    same keyword arguments with the same performance guarantees.

    See the docstring for ``pandas.read_csv`` for more information on available
    keyword arguments.

    Note that this function may fail if a CSV file includes quoted strings that
    contain the line terminator.

    Parameters
    ----------

    urlpath: string
        Absolute or relative filepath, URL (may include protocols like
        ``s3://``), or globstring for CSV files.
    blocksize: int or None
        Number of bytes by which to cut up larger files. Default value is
        computed based on available physical memory and the number of cores.
        If ``None``, use a single block for each file.
    collection: boolean
        Return a dask.dataframe if True or list of dask.delayed objects if False
    sample: int
        Number of bytes to use when determining dtypes
    storage_options: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.
    **kwargs: dict
        Options to pass down to ``pandas.read_csv``
    """
    if lineterminator is not None and len(lineterminator) == 1:
        kwargs['lineterminator'] = lineterminator
    else:
        lineterminator = '\n'
    if 'index' in kwargs or 'index_col' in kwargs:
        raise ValueError("Keyword 'index' not supported "
                         "dd.read_csv(...).set_index('my-index') instead")
    for kw in ['iterator', 'chunksize']:
        if kw in kwargs:
            raise ValueError("%s not supported for dd.read_csv" % kw)
    if kwargs.get('nrows', None):
        raise ValueError("The 'nrows' keyword is not supported by "
                         "`dd.read_csv`. To achieve the same behavior, it's "
                         "recommended to use `dd.read_csv(...).head(n=nrows)`")
    if isinstance(kwargs.get('skiprows'), list):
        raise TypeError("List of skiprows not supported for dd.read_csv")
    if isinstance(kwargs.get('header'), list):
        raise TypeError("List of header rows not supported for dd.read_csv")

    if blocksize and compression not in seekable_files:
        warn("Warning %s compression does not support breaking apart files\n"
             "Please ensure that each individual file can fit in memory and\n"
             "use the keyword ``blocksize=None to remove this message``\n"
             "Setting ``blocksize=None``" % compression)
        blocksize = None
    if compression not in seekable_files and compression not in cfiles:
        raise NotImplementedError("Compression format %s not installed" %
                                  compression)

    b_lineterminator = lineterminator.encode()
    sample, values = read_bytes(urlpath, delimiter=b_lineterminator,
                                         blocksize=blocksize,
                                         sample=sample,
                                         compression=compression,
                                         **(storage_options or {}))

    if not isinstance(values[0], (tuple, list)):
        values = [values]

    if kwargs.get('header', 'infer') is None:
        header = b''
    else:
        header = sample.split(b_lineterminator)[0] + b_lineterminator

    head = pd.read_csv(BytesIO(sample), **kwargs)

    df = read_csv_from_bytes(values, header, head, kwargs,
                             collection=collection, enforce=enforce)

    return df
