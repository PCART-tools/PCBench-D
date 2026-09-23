def open_files(path, s3=None, **kwargs):
    """ Open many files.  Return delayed objects.

    See Also
    --------
    dask.bytes.core.open_files:  User function
    """
    bucket = kwargs.pop('host', '')
    s3_path = bucket + path
    if s3 is None:
        s3 = _get_s3(**kwargs)

    filenames = sorted(s3.glob(s3_path))
    myopen = delayed(s3_open_file)
    s3_storage_options = s3.get_delegated_s3pars()

    return [myopen(_s3_path,
                   dask_key_name='s3-open-file-%s' % s3.info(_s3_path)['ETag'],
                   **s3_storage_options)
            for _s3_path in filenames]
