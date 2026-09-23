def open_files(path):
    """ Open many files.  Return delayed objects.

    See Also
    --------
    dask.bytes.core.open_files: User function
    """
    myopen = delayed(open)
    filepaths = sorted(glob(path))
    return [myopen(_path, mode='rb',
                   dask_key_name='open-%s' % tokenize(_path,
                                                      os.path.getmtime(_path)))
            for _path in filepaths]
