def freeze(d):
    """Freeze container to hashable form
    >>> freeze(1)
    1
    >>> freeze([1, 2])
    (1, 2)
    >>> freeze({1: 2})  # doctest: +SKIP
    frozenset([(1, 2)])
    """
    if isinstance(d, dict):
        return frozenset(map(freeze, d.items()))
    if isinstance(d, set):
        return frozenset(map(freeze, d))
    if isinstance(d, (tuple, list)):
        return tuple(map(freeze, d))
    return d
