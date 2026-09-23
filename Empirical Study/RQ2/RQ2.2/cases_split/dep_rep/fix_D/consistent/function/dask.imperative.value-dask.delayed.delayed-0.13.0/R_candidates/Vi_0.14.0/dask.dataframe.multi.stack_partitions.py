def stack_partitions(dfs, divisions, join='outer'):
    """Concatenate partitions on axis=0 by doing a simple stack"""
    meta = methods.concat([df._meta for df in dfs], join=join)
    empty = strip_unknown_categories(meta)

    name = 'concat-{0}'.format(tokenize(*dfs))
    dsk = {}
    i = 0
    for df in dfs:
        dsk.update(df.dask)
        # An error will be raised if the schemas or categories don't match. In
        # this case we need to pass along the meta object to transform each
        # partition, so they're all equivalent.
        try:
            df._meta == meta
            match = True
        except (ValueError, TypeError):
            match = False

        for key in df._keys():
            if match:
                dsk[(name, i)] = key
            else:
                dsk[(name, i)] = (methods.concat, [empty, key], 0, join)
            i += 1

    return new_dd_object(dsk, name, meta, divisions)
