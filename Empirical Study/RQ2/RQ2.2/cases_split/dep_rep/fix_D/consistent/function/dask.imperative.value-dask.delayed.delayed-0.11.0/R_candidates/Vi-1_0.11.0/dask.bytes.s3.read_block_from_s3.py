def read_block_from_s3(path, offset, length, s3=None,
                       delimiter=None, compression=None, **kwargs):
    bucket = kwargs.pop('host', '')
    s3_path = bucket + path
    if s3 is None:
        s3 = _get_s3(**kwargs)
    with s3.open(s3_path, 'rb') as f:
        if compression:
            f = compress_files[compression](f)
        try:
            result = read_block(f, offset, length, delimiter)
        finally:
            f.close()
    return result
