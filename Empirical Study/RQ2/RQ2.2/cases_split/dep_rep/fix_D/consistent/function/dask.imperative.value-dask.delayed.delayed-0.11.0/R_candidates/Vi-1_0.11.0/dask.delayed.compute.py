def compute(*args, **kwargs):
    """Evaluate more than one ``Delayed`` at once.

    Note that the only difference between this function and
    ``dask.base.compute`` is that this implicitly wraps python objects in
    ``Delayed``, allowing for collections of dask objects to be computed.

    Examples
    --------
    >>> a = value(1)
    >>> b = a + 2
    >>> c = a + 3
    >>> compute(b, c)  # Compute both simultaneously
    (3, 4)
    >>> compute(a, [b, c])  # Works for lists of Delayed
    (1, [3, 4])
    """
    args = [delayed(a) for a in args]
    return base.compute(*args, **kwargs)
