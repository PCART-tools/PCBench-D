def call_function(func, func_token, args, kwargs, pure=False, nout=None):
    dask_key_name = kwargs.pop('dask_key_name', None)
    pure = kwargs.pop('pure', pure)

    if dask_key_name is None:
        name = '%s-%s' % (funcname(func),
                          tokenize(func_token, *args, pure=pure, **kwargs))
    else:
        name = dask_key_name

    args, dasks = unzip(map(to_task_dask, args), 2)
    dsk = sharedict.merge(*dasks)
    if kwargs:
        dask_kwargs, dsk2 = to_task_dask(kwargs)
        dsk.update(dsk2)
        task = (apply, func, list(args), dask_kwargs)
    else:
        task = (func,) + args

    dsk.update_with_key({name: task}, key=name)
    nout = nout if nout is not None else None
    return Delayed(name, dsk, length=nout)
