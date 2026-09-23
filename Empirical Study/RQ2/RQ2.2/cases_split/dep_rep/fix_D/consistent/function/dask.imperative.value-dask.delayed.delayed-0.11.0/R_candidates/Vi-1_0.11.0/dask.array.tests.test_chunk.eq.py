def eq(a, b):
    c = a == b
    if isinstance(c, np.ndarray):
        c = c.all()
    return c
