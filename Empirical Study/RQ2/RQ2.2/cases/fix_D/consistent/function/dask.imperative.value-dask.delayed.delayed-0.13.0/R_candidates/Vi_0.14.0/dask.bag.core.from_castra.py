def from_castra(x, columns=None, index=False):
    """Load a dask Bag from a Castra.

    Parameters
    ----------
    x : filename or Castra
    columns: list or string, optional
        The columns to load. Default is all columns.
    index: bool, optional
        If True, the index is included as the first element in each tuple.
        Default is False.
    """
    from castra import Castra
    if not isinstance(x, Castra):
        x = Castra(x, readonly=True)
    elif not x._readonly:
        x = Castra(x.path, readonly=True)
    if columns is None:
        columns = x.columns

    name = 'from-castra-' + tokenize(os.path.getmtime(x.path), x.path,
                                     columns, index)
    dsk = dict(((name, i), (load_castra_partition, x, part, columns, index))
               for i, part in enumerate(x.partitions))
    return Bag(dsk, name, len(x.partitions))
