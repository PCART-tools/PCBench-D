def _partitions_of_index_values(divisions, values):
    """ Return defaultdict of division and values pairs
    Each key corresponds to the division which values are index values belong
    to the division.

    >>> sorted(_partitions_of_index_values([0, 5, 10], [3]).items())
    [(0, [3])]
    >>> sorted(_partitions_of_index_values([0, 5, 10], [3, 8, 5]).items())
    [(0, [3]), (1, [8, 5])]
    """
    if divisions[0] is None:
        msg = "Can not use loc on DataFrame without known divisions"
        raise ValueError(msg)

    results = defaultdict(list)
    values = pd.Index(values, dtype=object)
    for val in values:
        i = bisect.bisect_right(divisions, val)
        div = min(len(divisions) - 2, max(0, i - 1))
        results[div].append(val)
    return results
