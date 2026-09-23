def ndeepmap(n, func, seq):
    """ Call a function on every element within a nested container

    >>> def inc(x):
    ...     return x + 1
    >>> L = [[1, 2], [3, 4, 5]]
    >>> ndeepmap(2, inc, L)
    [[2, 3], [4, 5, 6]]
    """
    if n == 1:
        return [func(item) for item in seq]
    elif n > 1:
        return [ndeepmap(n - 1, func, item) for item in seq]
    else:
        return func(seq)
