def bag_zip(*bags):
    """ Partition-wise bag zip

    All passed bags must have the same number of partitions.

    NOTE: corresponding partitions should have the same length; if they do not,
    the "extra" elements from the longer partition(s) will be dropped.  If you
    have this case chances are that what you really need is a data alignment
    mechanism like pandas's, and not a missing value filler like zip_longest.

    Examples
    --------

    Correct usage:

    >>> import dask.bag as db
    >>> evens = db.from_sequence(range(0, 10, 2), partition_size=4)
    >>> odds = db.from_sequence(range(1, 10, 2), partition_size=4)
    >>> pairs = db.zip(evens, odds)
    >>> list(pairs)
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]

    Incorrect usage:

    >>> numbers = db.range(20) # doctest: +SKIP
    >>> fizz = numbers.filter(lambda n: n % 3 == 0) # doctest: +SKIP
    >>> buzz = numbers.filter(lambda n: n % 5 == 0) # doctest: +SKIP
    >>> fizzbuzz = db.zip(fizz, buzz) # doctest: +SKIP
    >>> list(fizzbuzzz) # doctest: +SKIP
    [(0, 0), (3, 5), (6, 10), (9, 15), (12, 20), (15, 25), (18, 30)]

    When what you really wanted was more along the lines of the following:

    >>> list(fizzbuzzz) # doctest: +SKIP
    [(0, 0), (3, None), (None, 5), (6, None), (None 10), (9, None),
    (12, None), (15, 15), (18, None), (None, 20), (None, 25), (None, 30)]
    """
    npartitions = bags[0].npartitions
    assert all(bag.npartitions == npartitions for bag in bags)
    # TODO: do more checks

    name = 'zip-' + tokenize(*bags)
    dsk = dict(
        ((name, i), (reify, (zip,) + tuple((bag.name, i) for bag in bags)))
        for i in range(npartitions))
    bags_dsk = merge(*(bag.dask for bag in bags))
    return Bag(merge(bags_dsk, dsk), name, npartitions)
