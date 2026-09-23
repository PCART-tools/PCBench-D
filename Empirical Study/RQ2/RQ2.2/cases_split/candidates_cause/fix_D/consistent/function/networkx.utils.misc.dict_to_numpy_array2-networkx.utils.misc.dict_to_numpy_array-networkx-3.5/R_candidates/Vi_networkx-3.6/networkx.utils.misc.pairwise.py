def pairwise(iterable, cyclic=False):
    """Return successive overlapping pairs taken from an input iterable.

    Parameters
    ----------
    iterable : iterable
        An iterable from which to generate pairs.

    cyclic : bool, optional (default=False)
        If `True`, a pair with the last and first items is included at the end.

    Returns
    -------
    iterator
        An iterator over successive overlapping pairs from the `iterable`.

    See Also
    --------
    itertools.pairwise

    Examples
    --------
    >>> list(nx.utils.pairwise([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    >>> list(nx.utils.pairwise([1, 2, 3, 4], cyclic=True))
    [(1, 2), (2, 3), (3, 4), (4, 1)]
    """
    if not cyclic:
        return itertools.pairwise(iterable)
    a, b = tee(iterable)
    first = next(b, None)
    return zip(a, chain(b, (first,)))
