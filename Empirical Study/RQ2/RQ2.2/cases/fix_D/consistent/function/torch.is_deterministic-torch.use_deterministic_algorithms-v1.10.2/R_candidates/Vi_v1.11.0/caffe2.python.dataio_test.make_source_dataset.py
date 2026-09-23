def make_source_dataset(ws, size=100, offset=0, name=None):
    name = name or "src"
    src_init = core.Net("{}_init".format(name))
    with core.NameScope(name):
        src_values = Struct(('label', np.array(range(offset, offset + size))))
        src_blobs = NewRecord(src_init, src_values)
        src_ds = Dataset(src_blobs, name=name)
        FeedRecord(src_blobs, src_values, ws)
    ws.run(src_init)
    return src_ds
