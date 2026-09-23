def test_overlap_few_dimensions_small():
    x = da.ones((20, 20), chunks=(10, 10))

    a = x.map_overlap(lambda x: x, depth={0: 1})
    assert_eq(x, a)
    assert any(isinstance(k[1], float) for k in a.dask)
    assert all(isinstance(k[2], int) for k in a.dask)

    b = x.map_overlap(lambda x: x, depth={1: 1})
    assert_eq(x, b)
    assert all(isinstance(k[1], int) for k in b.dask)
    assert any(isinstance(k[2], float) for k in b.dask)

    c = x.map_overlap(lambda x: x, depth={0: 1, 1: 1})
    assert_eq(x, c)
    assert any(isinstance(k[1], float) for k in c.dask)
    assert any(isinstance(k[2], float) for k in c.dask)
