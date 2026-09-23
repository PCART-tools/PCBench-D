def _set_option(*args, **kwargs):
    # must at least 1 arg deal with constraints later
    nargs = len(args)
    if not nargs or nargs % 2 != 0:
        raise ValueError("Must provide an even number of non-keyword "
                             "arguments")

    # default to false
    silent = kwargs.pop('silent', False)

    if kwargs:
        raise TypeError('_set_option() got an unexpected keyword '
                'argument "{0}"'.format(list(kwargs.keys())[0]))

    for k, v in zip(args[::2], args[1::2]):
        key = _get_single_key(k, silent)

        o = _get_registered_option(key)
        if o and o.validator:
            o.validator(v)

        # walk the nested dict
        root, k = _get_root(key)
        root[k] = v

        if o.cb:
            o.cb(key)
