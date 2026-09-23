def test_attr_optimize():
    # Check that attribute access is inlined
    a = delayed([1, 2, 3])
    o = a.index(1)
    dsk = o._optimize(o.dask, o._keys())
    assert getattr not in set(v[0] for v in dsk.values())
