def to_csv(df, filename, name_function=None, compression=None, compute=True,
           get=None, **kwargs):
    """
    Store Dask DataFrame to CSV files

    One filename per partition will be created. You can specify the
    filenames in a variety of ways.

    Use a globstring::

    >>> df.to_csv('/path/to/data/export-*.csv')  # doctest: +SKIP

    The * will be replaced by the increasing sequence 0, 1, 2, ...

    ::

        /path/to/data/export-0.csv
        /path/to/data/export-1.csv

    Use a globstring and a ``name_function=`` keyword argument.  The
    name_function function should expect an integer and produce a string.
    Strings produced by name_function must preserve the order of their
    respective partition indices.

    >>> from datetime import date, timedelta
    >>> def name(i):
    ...     return str(date(2015, 1, 1) + i * timedelta(days=1))

    >>> name(0)
    '2015-01-01'
    >>> name(15)
    '2015-01-16'

    >>> df.to_csv('/path/to/data/export-*.csv', name_function=name)  # doctest: +SKIP

    ::

        /path/to/data/export-2015-01-01.csv
        /path/to/data/export-2015-01-02.csv
        ...

    You can also provide an explicit list of paths::

    >>> paths = ['/path/to/data/alice.csv', '/path/to/data/bob.csv', ...]  # doctest: +SKIP
    >>> df.to_csv(paths) # doctest: +SKIP

    Parameters
    ----------
    filename : string
        Path glob indicating the naming scheme for the output files
    name_function : callable, default None
        Function accepting an integer (partition index) and producing a
        string to replace the asterisk in the given filename globstring.
        Should preserve the lexicographic order of partitions
    compression : string or None
        String like 'gzip' or 'xz'.  Must support efficient random access.
        Filenames with extensions corresponding to known compression
        algorithms (gz, bz2) will be compressed accordingly automatically
    sep : character, default ','
        Field delimiter for the output file
    na_rep : string, default ''
        Missing data representation
    float_format : string, default None
        Format string for floating point numbers
    columns : sequence, optional
        Columns to write
    header : boolean or list of string, default True
        Write out column names. If a list of string is given it is assumed
        to be aliases for the column names
    index : boolean, default True
        Write row names (index)
    index_label : string or sequence, or False, default None
        Column label for index column(s) if desired. If None is given, and
        `header` and `index` are True, then the index names are used. A
        sequence should be given if the DataFrame uses MultiIndex.  If
        False do not print fields for index names. Use index_label=False
        for easier importing in R
    nanRep : None
        deprecated, use na_rep
    mode : str
        Python write mode, default 'w'
    encoding : string, optional
        A string representing the encoding to use in the output file,
        defaults to 'ascii' on Python 2 and 'utf-8' on Python 3.
    compression : string, optional
        a string representing the compression to use in the output file,
        allowed values are 'gzip', 'bz2', 'xz',
        only used when the first argument is a filename
    line_terminator : string, default '\\n'
        The newline character or character sequence to use in the output
        file
    quoting : optional constant from csv module
        defaults to csv.QUOTE_MINIMAL
    quotechar : string (length 1), default '\"'
        character used to quote fields
    doublequote : boolean, default True
        Control quoting of `quotechar` inside a field
    escapechar : string (length 1), default None
        character used to escape `sep` and `quotechar` when appropriate
    chunksize : int or None
        rows to write at a time
    tupleize_cols : boolean, default False
        write multi_index columns as a list of tuples (if True)
        or new (expanded format) if False)
    date_format : string, default None
        Format string for datetime objects
    decimal: string, default '.'
        Character recognized as decimal separator. E.g. use ',' for
        European data
    """
    values = [_to_csv_chunk(d, **kwargs) for d in df.to_delayed()]
    values = write_bytes(values, filename, name_function, compression,
                         encoding=None)

    if compute:
        from dask import compute
        compute(*values, get=get)
    else:
        return values
