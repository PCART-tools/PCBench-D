def quote(x):
    """ Ensure that this value remains this value in a dask graph

    Some values in dask graph take on special meaning. Sometimes we want to
    ensure that our data is not interpreted but remains literal.

    >>> quote((add, 1, 2))  # doctest: +SKIP
    (tuple, [add, 1, 2])
    """
    if istask(x):
        return (tuple, list(map(quote, x)))
    return x
