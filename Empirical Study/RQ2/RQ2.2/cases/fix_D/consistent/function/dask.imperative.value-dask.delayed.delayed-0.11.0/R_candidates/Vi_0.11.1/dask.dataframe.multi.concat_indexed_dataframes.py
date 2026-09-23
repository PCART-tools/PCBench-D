def concat_indexed_dataframes(dfs, axis=0, join='outer'):
    """ Concatenate indexed dataframes together along the index """

    if join not in ('inner', 'outer'):
        raise ValueError("'join' must be 'inner' or 'outer'")

    from dask.dataframe.core import _emulate
    meta = _emulate(pd.concat, dfs, axis=axis, join=join)

    dfs = _maybe_from_pandas(dfs)
    dfs2, divisions, parts = align_partitions(*dfs)
    empties = [df._meta for df in dfs]

    parts2 = [[df if df is not None else empty
               for df, empty in zip(part, empties)]
              for part in parts]

    name = 'concat-indexed-' + tokenize(join, *dfs)
    dsk = dict(((name, i), (_pdconcat, part, axis, join))
                for i, part in enumerate(parts2))

    return new_dd_object(toolz.merge(dsk, *[df.dask for df in dfs2]),
                         name, meta, divisions)
