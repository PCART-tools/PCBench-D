def _factorize_from_iterables(iterables):
    """
    A higher-level wrapper over `_factorize_from_iterable`.

    *This is an internal function*

    Parameters
    ----------
    iterables : list-like of list-likes

    Returns
    -------
    codes_tuple : tuple of ndarrays
    categories_tuple : tuple of Indexes

    Notes
    -----
    See `_factorize_from_iterable` for more info.
    """
    if len(iterables) == 0:
        # For consistency, it should return a list of 2 tuples.
        return [(), ()]
    return lzip(*[_factorize_from_iterable(it) for it in iterables])
