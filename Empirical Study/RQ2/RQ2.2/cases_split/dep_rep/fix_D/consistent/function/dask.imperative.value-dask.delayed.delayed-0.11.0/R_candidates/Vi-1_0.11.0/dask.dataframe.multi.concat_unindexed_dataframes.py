def concat_unindexed_dataframes(dfs):
    name = 'concat-' + tokenize(*dfs)

    dsk = {(name, i): (concat_and_check, [(df._name, i) for df in dfs])
            for i in range(dfs[0].npartitions)}

    meta = pd.concat([df._meta for df in dfs], axis=1)

    return new_dd_object(toolz.merge(dsk, *[df.dask for df in dfs]),
                         name, meta, dfs[0].divisions)
