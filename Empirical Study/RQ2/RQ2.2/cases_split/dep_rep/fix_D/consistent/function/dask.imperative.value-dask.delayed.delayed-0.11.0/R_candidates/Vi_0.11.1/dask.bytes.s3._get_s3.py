def _get_s3(key=None, username=None, secret=None, password=None, **kwargs):
    """ Reuse ``s3`` instance or construct a new S3FileSystem from storage_options.

    >>> isinstance(_get_s3(), S3FileSystem)
    True
    >>> s3 = _get_s3(anon=False)
    >>> s3.anon
    False
    """
    if username is not None:
        if key is not None:
            raise KeyError("S3 storage options got secrets argument "
                           "collision. Please, use either `key` "
                           "storage option or password field in URLpath, "
                           "not both options together.")
        key = username
    if key is not None:
        kwargs['key'] = key
    if password is not None:
        if secret is not None:
            raise KeyError("S3 storage options got secrets argument "
                           "collision. Please, use either `secret` "
                           "storage option or password field in URLpath, "
                           "not both options together.")
        secret = password
    if secret is not None:
        kwargs['secret'] = secret
    return S3FileSystem(**kwargs)
