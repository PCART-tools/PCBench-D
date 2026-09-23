def call_function(func, args, kwargs, pure=False, nout=None):
    dask_key_name = kwargs.pop('dask_key_name', None)
    pure = kwargs.pop('pure', pure)

    if dask_key_name is None:
        name = '%s-%s' % (funcname(func), tokenize(func, *args,
                                                   pure=pure, **kwargs))
    else:
        name = dask_key_name

    args, dasks = unzip(map(to_task_dasks, args), 2)
    if kwargs:
        dask_kwargs, dasks2 = to_task_dasks(kwargs)
        dasks = dasks + (dasks2,)
        task = (apply, func, list(args), dask_kwargs)
    else:
        task = (func,) + args

    dasks = flat_unique(dasks)
    dasks.append({name: task})
    nout = nout if nout and nout > 1 else None
    return Delayed(name, dasks, length=nout)
