def partial_by_order(*args, **kwargs):
    """

    >>> partial_by_order(5, function=add, other=[(1, 10)])
    15
    """
    function = kwargs.pop('function')
    other = kwargs.pop('other')
    args2 = list(args)
    for i, arg in other:
        args2.insert(i, arg)
    return function(*args2, **kwargs)
