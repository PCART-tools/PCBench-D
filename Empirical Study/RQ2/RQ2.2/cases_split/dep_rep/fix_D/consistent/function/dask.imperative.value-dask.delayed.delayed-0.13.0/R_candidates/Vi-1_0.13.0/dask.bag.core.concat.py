def concat(bags):
    """ Concatenate many bags together, unioning all elements

    >>> import dask.bag as db
    >>> a = db.from_sequence([1, 2, 3])
    >>> b = db.from_sequence([4, 5, 6])
    >>> c = db.concat([a, b])

    >>> list(c)
    [1, 2, 3, 4, 5, 6]
    """
    name = 'concat-' + tokenize(*bags)
    counter = itertools.count(0)
    dsk = dict(((name, next(counter)), key)
               for bag in bags for key in sorted(bag._keys()))
    return Bag(merge(dsk, *[b.dask for b in bags]), name, len(dsk))
