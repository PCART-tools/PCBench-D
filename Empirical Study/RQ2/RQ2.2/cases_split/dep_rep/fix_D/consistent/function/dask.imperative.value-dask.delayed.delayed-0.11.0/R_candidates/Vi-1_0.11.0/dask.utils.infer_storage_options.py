def infer_storage_options(urlpath, inherit_storage_options=None):
    """ Infer storage options from URL path and merge it with existing storage
    options.

    Parameters
    ----------
    urlpath: str or unicode
        Either local absolute file path or URL (hdfs://namenode:8020/file.csv)
    storage_options: dict (optional)
        Its contents will get merged with the infered information from the
        given path

    Returns
    -------
    Storage options dict.

    Examples
    --------
    >>> infer_storage_options('/mnt/datasets/test.csv')  # doctest: +SKIP
    {"protocol": "file", "path", "/mnt/datasets/test.csv"}
    >>> infer_storage_options(
    ...          'hdfs://username:pwd@node:123/mnt/datasets/test.csv?q=1',
    ...          inherit_storage_options={'extra': 'value'})  # doctest: +SKIP
    {"protocol": "hdfs", "username": "username", "password": "pwd",
    "host": "node", "port": 123, "path": "/mnt/datasets/test.csv",
    "url_query": "q=1", "extra": "value"}
    """
    # Handle Windows paths including disk name in this special case
    if re.match(r'^[a-zA-Z]:\\', urlpath):
        return {'protocol': 'file',
                'path': urlpath}

    parsed_path = urlsplit(urlpath)

    inferred_storage_options = {
        'protocol': parsed_path.scheme or 'file',
        'path': parsed_path.path,
    }

    if parsed_path.netloc:
        # Parse `hostname` from netloc manually because `parsed_path.hostname`
        # lowercases the hostname which is not always desirable (e.g. in S3):
        # https://github.com/dask/dask/issues/1417
        inferred_storage_options['host'] = parsed_path.netloc.rsplit('@', 1)[-1].rsplit(':', 1)[0]
        if parsed_path.port:
            inferred_storage_options['port'] = parsed_path.port
        if parsed_path.username:
            inferred_storage_options['username'] = parsed_path.username
        if parsed_path.password:
            inferred_storage_options['password'] = parsed_path.password

    if parsed_path.query:
        inferred_storage_options['url_query'] = parsed_path.query
    if parsed_path.fragment:
        inferred_storage_options['url_fragment'] = parsed_path.fragment

    if inherit_storage_options:
        if set(inherit_storage_options) & set(inferred_storage_options):
            raise KeyError("storage options (%r) and path url options (%r) "
                           "collision is detected"
                           % (inherit_storage_options, inferred_storage_options))
        inferred_storage_options.update(inherit_storage_options)

    return inferred_storage_options
