def to_textfiles(b, path, name_function=None, compression='infer',
                 encoding=system_encoding, compute=True):
    """ Write bag to disk, one filename per partition, one line per element

    **Paths**: This will create one file for each partition in your bag. You
    can specify the filenames in a variety of ways.

    Use a globstring

    >>> b.to_textfiles('/path/to/data/*.json.gz')  # doctest: +SKIP

    The * will be replaced by the increasing sequence 1, 2, ...

    ::

        /path/to/data/0.json.gz
        /path/to/data/1.json.gz

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

    >>> b.to_textfiles('/path/to/data/*.json.gz', name_function=name)  # doctest: +SKIP

    ::

        /path/to/data/2015-01-01.json.gz
        /path/to/data/2015-01-02.json.gz
        ...

    You can also provide an explicit list of paths.

    >>> paths = ['/path/to/data/alice.json.gz', '/path/to/data/bob.json.gz', ...]  # doctest: +SKIP
    >>> b.to_textfiles(paths) # doctest: +SKIP

    **Compression**: Filenames with extensions corresponding to known
    compression algorithms (gz, bz2) will be compressed accordingly.

    **Bag Contents**: The bag calling ``to_textfiles`` must be a bag of
    text strings. For example, a bag of dictionaries could be written to
    JSON text files by mapping ``json.dumps`` on to the bag first, and
    then calling ``to_textfiles`` :

    >>> b_dict.map(json.dumps).to_textfiles("/path/to/data/*.json")  # doctest: +SKIP
    """
    out = write_bytes(b.to_delayed(), path, name_function, compression,
                      encoding=encoding)
    if compute:
        from dask import compute
        compute(*out)
    else:
        return out
