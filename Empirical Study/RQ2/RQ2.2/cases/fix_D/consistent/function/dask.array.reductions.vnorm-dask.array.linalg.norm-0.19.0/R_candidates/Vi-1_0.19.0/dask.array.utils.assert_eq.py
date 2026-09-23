def assert_eq(a, b, check_shape=True, **kwargs):
    a_original = a
    b_original = b
    if isinstance(a, Array):
        assert a.dtype is not None
        adt = a.dtype
        _check_dsk(a.dask)
        a = a.compute(scheduler='sync')
        if hasattr(a, 'todense'):
            a = a.todense()
        if not hasattr(a, 'dtype'):
            a = np.array(a, dtype='O')
        if _not_empty(a):
            assert a.dtype == a_original.dtype
        if check_shape:
            assert_eq_shape(a_original.shape, a.shape, check_nan=False)
    else:
        if not hasattr(a, 'dtype'):
            a = np.array(a, dtype='O')
        adt = getattr(a, 'dtype', None)

    if isinstance(b, Array):
        assert b.dtype is not None
        bdt = b.dtype
        _check_dsk(b.dask)
        b = b.compute(scheduler='sync')
        if not hasattr(b, 'dtype'):
            b = np.array(b, dtype='O')
        if hasattr(b, 'todense'):
            b = b.todense()
        if _not_empty(b):
            assert b.dtype == b_original.dtype
        if check_shape:
            assert_eq_shape(b_original.shape, b.shape, check_nan=False)
    else:
        if not hasattr(b, 'dtype'):
            b = np.array(b, dtype='O')
        bdt = getattr(b, 'dtype', None)

    if str(adt) != str(bdt):
        diff = difflib.ndiff(str(adt).splitlines(), str(bdt).splitlines())
        raise AssertionError('string repr are different' + os.linesep +
                             os.linesep.join(diff))

    try:
        assert a.shape == b.shape
        assert allclose(a, b, **kwargs)
        return True
    except TypeError:
        pass

    c = a == b

    if isinstance(c, np.ndarray):
        assert c.all()
    else:
        assert c

    return True
