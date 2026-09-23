def get_fs_paths_myopen(urlpath, compression, mode, encoding='utf8',
                        num=1, name_function=None, **kwargs):
    if isinstance(urlpath, (str, unicode)):
        myopen = OpenFileCreator(urlpath, compression, text='b' not in mode,
                                 encoding=encoding, **kwargs)
        if 'w' in mode:
            paths = _expand_paths(urlpath, name_function, num)
        elif "*" in urlpath:
            paths = myopen.fs.glob(urlpath, **kwargs)
        else:
            paths = [urlpath]
    elif isinstance(urlpath, (list, set, tuple, dict)):
        myopen = OpenFileCreator(urlpath[0], compression, text='b' not in mode,
                                 encoding=encoding, **kwargs)
        paths = urlpath
    else:
        raise ValueError('url type not understood: %s' % urlpath)
    return myopen.fs, paths, myopen
