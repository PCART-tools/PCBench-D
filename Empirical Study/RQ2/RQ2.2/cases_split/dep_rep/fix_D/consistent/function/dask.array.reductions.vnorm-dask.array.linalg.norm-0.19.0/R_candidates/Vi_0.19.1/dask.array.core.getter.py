def getter(a, b, asarray=True, lock=None):
    if isinstance(b, tuple) and any(x is None for x in b):
        b2 = tuple(x for x in b if x is not None)
        b3 = tuple(None if x is None else slice(None, None)
                   for x in b if not isinstance(x, (int, long)))
        return getter(a, b2, asarray=asarray, lock=lock)[b3]

    if lock:
        lock.acquire()
    try:
        c = a[b]
        if asarray:
            c = np.asarray(c)
    finally:
        if lock:
            lock.release()
    return c
