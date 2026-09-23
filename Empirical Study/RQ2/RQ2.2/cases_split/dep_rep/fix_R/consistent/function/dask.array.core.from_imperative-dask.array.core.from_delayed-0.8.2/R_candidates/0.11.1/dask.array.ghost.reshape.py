def reshape(shape, seq):
    """ Reshape iterator to nested shape

    >>> reshape((2, 3), range(6))
    [[0, 1, 2], [3, 4, 5]]
    """
    if len(shape) == 1:
        return list(seq)
    else:
        n = int(len(seq) / shape[0])
        return [reshape(shape[1:], part) for part in partition(n, seq)]
