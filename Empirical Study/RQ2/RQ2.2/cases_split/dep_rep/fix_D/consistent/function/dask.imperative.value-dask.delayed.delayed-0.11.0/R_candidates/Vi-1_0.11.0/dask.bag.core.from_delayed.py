def from_delayed(values):
    """ Create bag from many dask.delayed objects

    Parameters
    ----------
    values: list of Values
        An iterable of dask.delayed.Value objects, such as come from dask.do
        These comprise the individual partitions of the resulting bag

    Returns
    -------
    Bag

    Examples
    --------
    >>> b = from_delayed([x, y, z])  # doctest: +SKIP
    """
    from dask.delayed import Value
    if isinstance(values, Value):
        values = [values]
    dsk = merge(v.dask for v in values)

    name = 'bag-from-delayed-' + tokenize(*values)
    names = [(name, i) for i in range(len(values))]
    values = [v.key for v in values]
    dsk2 = dict(zip(names, values))

    return Bag(merge(dsk, dsk2), name, len(values))
