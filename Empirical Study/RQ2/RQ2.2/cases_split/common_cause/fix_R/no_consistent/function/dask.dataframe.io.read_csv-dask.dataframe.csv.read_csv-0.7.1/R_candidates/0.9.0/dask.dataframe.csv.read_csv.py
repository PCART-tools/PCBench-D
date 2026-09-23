def read_csv(filename, blocksize=2**25, chunkbytes=None,
        collection=True, lineterminator='\n', compression=None,
        enforce_dtypes=True, sample=10000, **kwargs):
    """ Read CSV files into a Dask.DataFrame

    This parallelizes the ``pandas.read_csv`` file in the following ways:

    1.  It supports loading many files at once using globstrings as follows:

        >>> df = dd.read_csv('myfiles.*.csv')  # doctest: +SKIP

    2.  In some cases it can break up large files as follows:

        >>> df = dd.read_csv('largefile.csv', blocksize=25e6)  # 25MB chunks  # doctest: +SKIP

    Internally dd.read_csv uses pandas.read_csv and so supports many of the
    same keyword arguments with the same performance guarantees.

    See the docstring for ``pandas.read_csv`` for more information on available
    keyword arguments.

    Parameters
    ----------

    filename: string
        Filename or globstring for CSV files.  May include protocols like s3://
    blocksize: int or None
        Number of bytes by which to cut up larger files
    collection: boolean
        Return a dask.dataframe if True or list of dask.delayed objects if False
    sample: int
        Number of bytes to use when determining dtypes
    **kwargs: dict
        Options to pass down to ``pandas.read_csv``
    """
    if len(lineterminator) == 1:
        kwargs['lineterminator'] = lineterminator
    if chunkbytes is not None:
        warn("Deprecation warning: chunksize csv keyword renamed to blocksize")
        blocksize=chunkbytes
    if 'index' in kwargs or 'index_col' in kwargs:
        raise ValueError("Keyword 'index' not supported "
                         "dd.read_csv(...).set_index('my-index') instead")
    for kw in ['iterator', 'chunksize']:
        if kw in kwargs:
            raise ValueError("%s not supported for dd.read_csv" % kw)
    if isinstance(kwargs.get('skiprows'), list):
        raise TypeError("List of skiprows not supported for dd.read_csv")
    if isinstance(kwargs.get('header'), list):
        raise TypeError("List of header rows not supported for dd.read_csv")

    if blocksize and compression not in seekable_files:
        warn("Warning %s compression does not support breaking apart files\n"
             "Please ensure that each individiaul file can fit in memory and\n"
             "use the keyword ``blocksize=None to remove this message``\n"
             "Setting ``blocksize=None``" % compression)
        blocksize = None
    if compression not in seekable_files and compression not in cfiles:
        raise NotImplementedError("Compression format %s not installed" %
                                  compression)

    b_lineterminator = lineterminator.encode()
    sample, values = read_bytes(filename, delimiter=b_lineterminator,
                                          blocksize=blocksize,
                                          sample=sample, compression=compression)
    if not isinstance(values[0], (tuple, list)):
        values = [values]

    if 'nrows' in kwargs:
        values = [[values[0][0]]]

    if kwargs.get('header', 'infer') is None:
        header = b''
    else:
        header = sample.split(b_lineterminator)[0] + b_lineterminator
    head = pd.read_csv(BytesIO(sample), **kwargs)

    df = read_csv_from_bytes(values, header, head, kwargs,
            collection=collection, enforce_dtypes=enforce_dtypes)


    return df
