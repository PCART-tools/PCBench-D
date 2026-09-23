def issorted(seq):
    """ Is sequence sorted?

    >>> issorted([1, 2, 3])
    True
    >>> issorted([3, 1, 2])
    False
    """
    if len(seq) == 0:
        return True
    return np.all(seq[:-1] <= seq[1:])
