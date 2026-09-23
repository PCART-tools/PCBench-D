def open_file_write_direct(path, s3=None, **kwargs):
    bucket = kwargs.pop('host', '')
    if s3 is None:
        s3 = _get_s3(**kwargs)
    return s3.open(bucket + path, 'wb')
