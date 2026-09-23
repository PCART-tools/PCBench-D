def optimize(dsk, keys, fuse_keys=None, rename_fused_keys=True, **kwargs):
    """ Optimize a dask from a dask.bag """
    dsk2, dependencies = cull(dsk, keys)
    dsk3, dependencies = fuse(dsk2, keys + (fuse_keys or []), dependencies,
                              rename_fused_keys=rename_fused_keys)
    dsk4 = inline_singleton_lists(dsk3, dependencies)
    dsk5 = lazify(dsk4)
    return dsk5
