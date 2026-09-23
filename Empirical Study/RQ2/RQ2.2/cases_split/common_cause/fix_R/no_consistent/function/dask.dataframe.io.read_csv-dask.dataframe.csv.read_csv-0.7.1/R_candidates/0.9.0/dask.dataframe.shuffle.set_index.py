def set_index(df, index, npartitions=None, compute=True,
              drop=True, **kwargs):
    """ Set DataFrame index to new column

    Sorts index and realigns Dataframe to new sorted order.

    This shuffles and repartitions your data. If done in parallel the
    resulting order is non-deterministic.
    """
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

    divisions = (index2
                  .quantile(np.linspace(0, 1, npartitions + 1))
                  .compute()).tolist()

    return set_partition(df, index, divisions, compute=compute,
                         drop=drop, **kwargs)
