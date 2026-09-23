def eq(a, b):
    if isinstance(a, Array):
        a = a.compute(get=dask.get)
    if isinstance(b, Array):
        b = b.compute(get=dask.get)
    c = a == b
    if isinstance(c, np.ndarray):
        c = c.all()
    return c
