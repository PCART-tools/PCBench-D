def getarray(a, b, lock=None):
    """ Mimics getitem but includes call to np.asarray

    >>> getarray([1, 2, 3, 4, 5], slice(1, 4))
    array([2, 3, 4])
    """
    if isinstance(b, tuple) and any(x is None for x in b):
        b2 = tuple(x for x in b if x is not None)
        b3 = tuple(None if x is None else slice(None, None)
                   for x in b if not isinstance(x, (int, long)))
        return getarray(a, b2, lock)[b3]

    if lock:
        lock.acquire()
    try:
        c = a[b]
        if type(c) != np.ndarray:
            c = np.asarray(c)
    finally:
        if lock:
            lock.release()
    return c
