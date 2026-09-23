def digit(n, k, base):
    """

    >>> digit(1234, 0, 10)
    4
    >>> digit(1234, 1, 10)
    3
    >>> digit(1234, 2, 10)
    2
    >>> digit(1234, 3, 10)
    1
    """
    return n // base**k % base
