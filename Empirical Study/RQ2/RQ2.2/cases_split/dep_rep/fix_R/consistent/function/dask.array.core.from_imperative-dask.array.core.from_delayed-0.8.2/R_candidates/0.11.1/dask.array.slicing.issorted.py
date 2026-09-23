def issorted(seq):
    """ Is sequence sorted?

    >>> issorted([1, 2, 3])
    True
    >>> issorted([3, 1, 2])
    False
    """
    if not seq:
        return True
    x = seq[0]
    for elem in seq[1:]:
        if elem < x:
            return False
        x = elem
    return True
