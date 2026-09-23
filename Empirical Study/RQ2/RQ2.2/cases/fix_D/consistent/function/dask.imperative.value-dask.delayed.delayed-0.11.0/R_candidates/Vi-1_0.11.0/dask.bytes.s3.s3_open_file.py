def s3_open_file(path, s3=None, **kwargs):
    bucket = kwargs.pop('host', '')
    s3_path = bucket + path
    if s3 is None:
        s3 = _get_s3(**kwargs)
    return s3.open(s3_path, mode='rb')
