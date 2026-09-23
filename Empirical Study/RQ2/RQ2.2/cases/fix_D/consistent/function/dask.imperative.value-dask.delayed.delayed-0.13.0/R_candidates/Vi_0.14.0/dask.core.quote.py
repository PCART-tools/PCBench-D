def quote(x):
    """ Ensure that this value remains this value in a dask graph

    Some values in dask graph take on special meaning. Sometimes we want to
    ensure that our data is not interpreted but remains literal.

    >>> quote((add, 1, 2))  # doctest: +SKIP
    (literal<type=tuple>,)
    """
    if istask(x) or type(x) is list:
        return (literal(x),)
    return x
