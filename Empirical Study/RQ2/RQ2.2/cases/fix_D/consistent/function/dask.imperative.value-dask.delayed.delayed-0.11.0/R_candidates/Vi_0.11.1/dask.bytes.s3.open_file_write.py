def open_file_write(paths, s3=None, **kwargs):
    """ Open list of files using delayed """
    bucket = kwargs.pop('host', '')
    if s3 is None:
        s3 = _get_s3(**kwargs)
    out = [delayed(s3.open)(bucket + path, 'wb') for path in paths]
    return out
