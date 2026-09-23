def optimize(dsk, keys, fuse_keys=None, **kwargs):
    """ Optimize a dask from a dask.bag """
    dsk2, dependencies = cull(dsk, keys)
    dsk3, dependencies = fuse(dsk2, keys + (fuse_keys or []), dependencies)
    dsk4 = inline_singleton_lists(dsk3, dependencies)
    dsk5 = lazify(dsk4)
    return dsk5
