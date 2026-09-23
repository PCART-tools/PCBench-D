def insert_many(seq, where, val):
    """ Insert value at many locations in sequence

    >>> insert_many(['a', 'b', 'c'], [0, 2], 'z')
    ('z', 'a', 'z', 'b', 'c')
    """
    seq = list(seq)
    result = []
    for i in range(len(where) + len(seq)):
        if i in where:
            result.append(val)
        else:
            result.append(seq.pop(0))
    return tuple(result)
