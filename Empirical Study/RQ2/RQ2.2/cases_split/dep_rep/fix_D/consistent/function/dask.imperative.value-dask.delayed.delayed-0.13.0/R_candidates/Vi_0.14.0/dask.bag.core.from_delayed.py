def from_delayed(values):
    """ Create bag from many dask.delayed objects

    These objects will become the partitions of the resulting Bag.  They should
    evaluate to a ``list`` or some other concrete sequence.

    Parameters
    ----------
    values: list of delayed values
        An iterable of dask Delayed objects.  Each evaluating to a list.

    Returns
    -------
    Bag

    Examples
    --------
    >>> x, y, z = [delayed(load_sequence_from_file)(fn)
    ...             for fn in filenames] # doctest: +SKIP
    >>> b = from_delayed([x, y, z])  # doctest: +SKIP

    See also
    --------
    dask.delayed
    """
    from dask.delayed import Delayed, delayed
    if isinstance(values, Delayed):
        values = [values]
    values = [delayed(v)
              if not isinstance(v, Delayed) and hasattr(v, 'key')
              else v
              for v in values]
    dsk = merge(v.dask for v in values)

    name = 'bag-from-delayed-' + tokenize(*values)
    names = [(name, i) for i in range(len(values))]
    values = [(reify, v.key) for v in values]
    dsk2 = dict(zip(names, values))

    return Bag(merge(dsk, dsk2), name, len(values))
