def value(val, name=None):
    """Create a ``Value`` from a python object.

    Parameters
    ----------
    val : object
        Object to be wrapped.
    name : string, optional
        Name to be used in the resulting dask.

    Examples
    --------
    >>> a = value([1, 2, 3])
    >>> a.compute()
    [1, 2, 3]

    Values can act as a proxy to the underlying object. Many operators are
    supported:

    >>> (a + [1, 2]).compute()
    [1, 2, 3, 1, 2]
    >>> a[1].compute()
    2

    Method and attribute access also works:

    >>> a.count(2).compute()
    1

    Note that if a method doesn't exist, no error will be thrown until runtime:

    >>> res = a.not_a_real_method()
    >>> res.compute()  # doctest: +SKIP
    AttributeError("'list' object has no attribute 'not_a_real_method'")

    Methods are assumed to be impure by default, meaning that subsequent calls
    may return different results. To assume purity, set `pure=True`. This
    allows sharing of any intermediate values.

    >>> a.count(2, pure=True).key == a.count(2, pure=True).key
    True
    """
    if isinstance(val, Value):
        return val
    task, dasks = to_task_dasks(val)
    name = name or (type(val).__name__ + '-' + tokenize(task, pure=True))
    dasks.append({name: task})
    return Value(name, dasks)
