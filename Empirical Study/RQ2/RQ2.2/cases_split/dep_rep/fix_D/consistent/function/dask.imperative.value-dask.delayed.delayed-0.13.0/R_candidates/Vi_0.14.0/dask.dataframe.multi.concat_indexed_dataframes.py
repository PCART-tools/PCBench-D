def concat_indexed_dataframes(dfs, axis=0, join='outer'):
    """ Concatenate indexed dataframes together along the index """
    meta = methods.concat([df._meta for df in dfs], axis=axis, join=join)
    empties = [strip_unknown_categories(df._meta) for df in dfs]

    dfs2, divisions, parts = align_partitions(*dfs)

    name = 'concat-indexed-' + tokenize(join, *dfs)

    parts2 = [[df if df is not None else empty
               for df, empty in zip(part, empties)]
              for part in parts]

    dsk = dict(((name, i), (methods.concat, part, axis, join))
               for i, part in enumerate(parts2))
    for df in dfs2:
        dsk.update(df.dask)

    return new_dd_object(dsk, name, meta, divisions)
