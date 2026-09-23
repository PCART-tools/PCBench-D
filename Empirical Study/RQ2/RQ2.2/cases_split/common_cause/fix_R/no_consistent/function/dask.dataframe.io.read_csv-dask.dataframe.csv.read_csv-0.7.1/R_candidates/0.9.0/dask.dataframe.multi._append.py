def _append(df, other, divisions):
    """ Internal function to append 2 dd.DataFrame/Series instances """
    # ToDo: might be possible to merge the logic to concat,
    token = tokenize(df, other)
    name = '{0}-append--{1}'.format(df._token_prefix, token)
    dsk = {}

    npart = df.npartitions
    for i in range(npart):
        dsk[(name, i)] = (df._name, i)
    for j in range(other.npartitions):
        dsk[(name, npart + j)] = (other._name, j)
    dsk = toolz.merge(dsk, df.dask, other.dask)
    dummy = df._pd.append(other._pd)
    return _Frame(dsk, name, dummy, divisions)
