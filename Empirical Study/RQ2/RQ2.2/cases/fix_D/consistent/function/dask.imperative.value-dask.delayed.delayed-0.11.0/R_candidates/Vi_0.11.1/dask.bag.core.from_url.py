def from_url(urls):
    """Create a dask.bag from a url

    Examples
    --------
    >>> a = from_url('http://raw.githubusercontent.com/dask/dask/master/README.rst')  # doctest: +SKIP
    >>> a.npartitions  # doctest: +SKIP
    1

    >>> a.take(8)  # doctest: +SKIP
    ('Dask\\n',
     '====\\n',
     '\\n',
     '|Build Status| |Coverage| |Doc Status| |Gitter|\\n',
     '\\n',
     'Dask provides multi-core execution on larger-than-memory datasets using blocked\\n',
     'algorithms and task scheduling.  It maps high-level NumPy and list operations\\n',
     'on large datasets on to graphs of many operations on small in-memory datasets.\\n')

    >>> b = from_url(['http://github.com', 'http://google.com'])  # doctest: +SKIP
    >>> b.npartitions  # doctest: +SKIP
    2
    """
    if isinstance(urls, str):
        urls = [urls]
    name = 'from_url-' + uuid.uuid4().hex
    dsk = {}
    for i, u in enumerate(urls):
        dsk[(name, i)] = (list, (urlopen, u))
    return Bag(dsk, name, len(urls))
