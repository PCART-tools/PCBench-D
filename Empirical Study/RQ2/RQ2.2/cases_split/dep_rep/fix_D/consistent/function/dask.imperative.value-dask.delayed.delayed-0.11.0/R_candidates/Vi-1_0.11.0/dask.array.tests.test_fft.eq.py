def eq(a, b):
    assert a.shape == b.shape, mismatch_err('shape', a.shape, b.shape)

    if isinstance(a, Array):
        adt = a._dtype
        a = a.compute(get=dask.get)
    else:
        adt = getattr(a, 'dtype', None)
    if isinstance(b, Array):
        bdt = b._dtype
        b = b.compute(get=dask.get)
    else:
        bdt = getattr(b, 'dtype', None)

    assert str(adt) == str(bdt), mismatch_err('dtype', str(adt), str(bdt))

    try:
        return np.allclose(a, b)
    except TypeError:
        pass

    c = a == b

    if isinstance(c, np.ndarray):
        return c.all()
    else:
        return c
