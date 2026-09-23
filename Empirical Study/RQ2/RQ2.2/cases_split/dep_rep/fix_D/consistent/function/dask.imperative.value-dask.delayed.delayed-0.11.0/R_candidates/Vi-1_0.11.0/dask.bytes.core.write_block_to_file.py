def write_block_to_file(data, f, compression, encoding):
    """
    Parameters
    ----------
    data : data to write
        Either str/bytes, or iterable producing those, or something file-like
        which can be read.
    f : file-like
        backend-dependent file-like object
    compression : string
        a key of `compress_files`
    encoding : string (None)
        if a string (e.g., 'ascii', 'utf8'), implies text mode, otherwise no
        encoding and binary mode.
    """
    original = False
    f2 = f
    f = SeekableFile(f)
    if compression:
        original = True
        f = compress_files[compression](f, mode='wb')
    try:
        if isinstance(data, (str, bytes)):
            if encoding:
                f.write(data.encode(encoding=encoding))
            else:
                f.write(data)
        elif isinstance(data, io.IOBase):
            # file-like
            out = '1'
            while out:
                out = data.read(64*2**10)
                if encoding:
                    f.write(out.encode(encoding=encoding))
                else:
                    f.write(out)
        else:
            # iterable, e.g., bag contents
            start = False
            for d in data:
                if start:
                    f.write(b'\n')
                else:
                    start = True
                if encoding:
                    f.write(d.encode(encoding=encoding))
                else:
                    f.write(d)
    finally:
        f.close()
        if original:
            f2.close()
