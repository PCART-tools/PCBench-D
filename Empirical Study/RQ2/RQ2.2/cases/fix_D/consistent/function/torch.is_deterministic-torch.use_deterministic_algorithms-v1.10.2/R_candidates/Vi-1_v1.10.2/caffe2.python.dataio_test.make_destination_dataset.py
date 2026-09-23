def make_destination_dataset(ws, schema, name=None):
    name = name or 'dst'
    dst_init = core.Net('{}_init'.format(name))
    with core.NameScope(name):
        dst_ds = Dataset(schema, name=name)
        dst_ds.init_empty(dst_init)
    ws.run(dst_init)
    return dst_ds
