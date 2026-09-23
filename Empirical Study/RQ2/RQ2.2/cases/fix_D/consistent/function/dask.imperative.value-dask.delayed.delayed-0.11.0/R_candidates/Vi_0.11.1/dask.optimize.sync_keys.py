def sync_keys(dsk1, dsk2):
    """Return a dict matching keys in `dsk2` to equivalent keys in `dsk1`.

    Parameters
    ----------
    dsk1, dsk2 : dict

    Examples
    --------
    >>> from operator import add, mul
    >>> dsk1 = {'a': 1, 'b': (add, 'a', 10), 'c': (mul, 'b', 5)}
    >>> dsk2 = {'x': 1, 'y': (add, 'x', 10), 'z': (mul, 'y', 2)}
    >>> sync_keys(dsk1, dsk2)   # doctest: +SKIP
    {'x': 'a', 'y': 'b'}
    """

    return _sync_keys(dsk1, dsk2, toposort(dsk2))
