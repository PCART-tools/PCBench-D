def _get_handle(path, mode, encoding=None, compression=None):
    """Gets file handle for given path and mode.
    NOTE: Under Python 3.2, getting a compressed file handle means reading in
    the entire file, decompressing it and decoding it to ``str`` all at once
    and then wrapping it in a StringIO.
    """
    if compression is not None:
        if encoding is not None and not compat.PY3:
            msg = 'encoding + compression not yet supported in Python 2'
            raise ValueError(msg)

        if compression == 'gzip':
            import gzip
            f = gzip.GzipFile(path, 'rb')
        elif compression == 'bz2':
            import bz2

            f = bz2.BZ2File(path, 'rb')
        else:
            raise ValueError('Unrecognized compression type: %s' %
                             compression)
        if compat.PY3_2:
            # gzip and bz2 don't work with TextIOWrapper in 3.2
            encoding = encoding or get_option('display.encoding')
            f = StringIO(f.read().decode(encoding))
        elif compat.PY3:
            from io import TextIOWrapper
            f = TextIOWrapper(f, encoding=encoding)
        return f
    else:
        if compat.PY3:
            if encoding:
                f = open(path, mode, encoding=encoding)
            else:
                f = open(path, mode, errors='replace')
        else:
            f = open(path, mode)

    return f
