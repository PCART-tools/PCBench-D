def from_sequence(seq, partition_size=None, npartitions=None):
    """ Create dask from Python sequence

    This sequence should be relatively small in memory.  Dask Bag works
    best when it handles loading your data itself.  Commonly we load a
    sequence of filenames into a Bag and then use ``.map`` to open them.

    Parameters
    ----------
    seq: Iterable
        A sequence of elements to put into the dask
    partition_size: int (optional)
        The length of each partition
    npartitions: int (optional)
        The number of desired partitions

    It is best to provide either ``partition_size`` or ``npartitions``
    (though not both.)

    Examples
    --------
    >>> b = from_sequence(['Alice', 'Bob', 'Chuck'], partition_size=2)

    See Also
    --------
    read_text: Create bag from textfiles
    """
    seq = list(seq)
    if npartitions and not partition_size:
        partition_size = int(math.ceil(len(seq) / npartitions))
    if npartitions is None and partition_size is None:
        if len(seq) < 100:
            partition_size = 1
        else:
            partition_size = int(len(seq) / 100)

    parts = list(partition_all(partition_size, seq))
    name = 'from_sequence-' + tokenize(seq, partition_size)
    d = dict(((name, i), list(part)) for i, part in enumerate(parts))
    return Bag(d, name, len(d))
