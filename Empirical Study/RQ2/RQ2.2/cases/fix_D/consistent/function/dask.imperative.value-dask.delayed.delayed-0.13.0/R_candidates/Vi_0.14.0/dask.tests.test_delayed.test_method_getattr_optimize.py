def test_method_getattr_optimize():
    a = delayed([1, 2, 3])
    o = a.index(1)
    dsk = o._optimize(o.dask, o._keys())
    # Don't getattr the method, then call in separate task
    assert getattr not in set(v[0] for v in dsk.values())
