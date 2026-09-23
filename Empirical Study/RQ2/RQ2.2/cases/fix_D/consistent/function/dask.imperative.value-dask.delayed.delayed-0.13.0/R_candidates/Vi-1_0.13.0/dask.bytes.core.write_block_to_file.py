def write_block_to_file(data, lazy_file):
    """
    Parameters
    ----------
    data : data to write
        Either str/bytes, or iterable producing those, or something file-like
        which can be read.
    lazy_file : file-like or file context
        gives writable backend-dependent file-like object when used with `with`
    """
    binary = 'b' in str(getattr(lazy_file, 'mode', 'b'))
    with lazy_file as f:
        if isinstance(f, io.TextIOWrapper):
            binary = False
        if binary:
            ensure = ensure_bytes
        else:
            ensure = ensure_unicode
        if isinstance(data, (str, bytes, unicode)):
            f.write(ensure(data))
        elif isinstance(data, io.IOBase):
            # file-like
            out = True
            while out:
                out = data.read(64 * 2 ** 10)
                f.write(ensure(out))
        else:
            # iterable, e.g., bag contents
            start = False
            for d in data:
                if start:
                    if binary:
                        try:
                            f.write(b'\n')
                        except TypeError:
                            binary = False
                            f.write('\n')
                    else:
                        f.write(u'\n')
                else:
                    start = True
                f.write(ensure(d))
