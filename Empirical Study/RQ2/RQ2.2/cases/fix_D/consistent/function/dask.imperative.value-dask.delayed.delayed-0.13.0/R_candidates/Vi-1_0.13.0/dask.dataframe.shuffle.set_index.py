def set_index(df, index, npartitions=None, shuffle=None, compute=False,
              drop=True, upsample=1.0, divisions=None, **kwargs):
    """ See _Frame.set_index for docstring """
    if (isinstance(index, Series) and index._name == df.index._name):
        return df
    if isinstance(index, (DataFrame, tuple, list)):
        raise NotImplementedError(
            "Dask dataframe does not yet support multi-indexes.\n"
            "You tried to index with this index: %s\n"
            "Indexes must be single columns only." % str(index))

    npartitions = npartitions or df.npartitions
    if not isinstance(index, Series):
        index2 = df[index]
    else:
        index2 = index

    if divisions is None:
        divisions = (index2
                     ._repartition_quantiles(npartitions, upsample=upsample)
                     .compute()).tolist()

    return set_partition(df, index, divisions, shuffle=shuffle, drop=drop,
                         compute=compute, **kwargs)
