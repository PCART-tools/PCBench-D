def partition_by_size(sizes, seq):
    """

    >>> partition_by_size([10, 20, 10], [1, 5, 9, 12, 29, 35])
    [[1, 5, 9], [2, 19], [5]]
    """
    seq = list(seq)
    pretotal = 0
    total = 0
    i = 0
    result = list()
    for s in sizes:
        total += s
        L = list()
        while i < len(seq) and seq[i] < total:
            L.append(seq[i] - pretotal)
            i += 1
        result.append(L)
        pretotal += s
    return result
