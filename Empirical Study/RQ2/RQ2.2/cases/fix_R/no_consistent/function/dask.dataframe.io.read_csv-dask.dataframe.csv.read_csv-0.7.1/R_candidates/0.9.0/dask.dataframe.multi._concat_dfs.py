def _concat_dfs(dfs, name, join='outer'):
    """ Internal function to concat dask dict and DataFrame.columns """
    dsk = dict()
    i = 0

    empties = [df._pd for df in dfs]
    dummy = pd.concat(empties, axis=0, join=join)

    if isinstance(dummy, pd.Series):
        # in this case, input must be all Series. No need to care DataFrame.
        columns = pd.Index([])
    else:
        columns = dummy.columns
        if len(columns) == 0:
            raise ValueError('Failed to concat, no columns remain')

    for df in dfs:
        if isinstance(df, DataFrame):
            # filter DataFrame columns
            if not columns.equals(df.columns):
                df = df[[c for c in columns if c in df.columns]]
        # Series must remain if output columns exist

        dsk = toolz.merge(dsk, df.dask)
        for key in df._keys():
            dsk[(name, i)] = key
            i += 1

    return dsk, dummy
