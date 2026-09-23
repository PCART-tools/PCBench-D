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
    if _read_parquet_row_group:
        dsk6 = fuse_getitem(dsk5, _read_parquet_row_group, 4)
    else:
        dsk6 = dsk5
    dsk7, _ = cull(dsk6, keys)
    return dsk7
