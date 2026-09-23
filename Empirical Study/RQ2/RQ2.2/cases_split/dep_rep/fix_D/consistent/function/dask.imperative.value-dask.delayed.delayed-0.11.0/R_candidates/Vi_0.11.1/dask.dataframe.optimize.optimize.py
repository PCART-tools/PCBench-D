def optimize(dsk, keys, **kwargs):
    if isinstance(keys, list):
        dsk2, dependencies = cull(dsk, list(core.flatten(keys)))
    else:
        dsk2, dependencies = cull(dsk, [keys])
    try:
        from castra import Castra
        dsk3 = fuse_getitem(dsk2, Castra.load_partition, 3)
        dsk4 = fuse_castra_index(dsk3)
    except ImportError:
        dsk4 = dsk2
    dsk5 = fuse_getitem(dsk4, dataframe_from_ctable, 3)
    dsk6, _ = cull(dsk5, keys)
    return dsk6
