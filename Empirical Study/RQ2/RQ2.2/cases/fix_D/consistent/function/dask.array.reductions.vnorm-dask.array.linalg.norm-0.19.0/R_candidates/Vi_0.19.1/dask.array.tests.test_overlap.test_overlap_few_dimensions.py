def test_overlap_few_dimensions():
    x = da.ones((100, 100), chunks=(10, 10))

    a = x.map_overlap(lambda x: x, depth={0: 1})
    b = x.map_overlap(lambda x: x, depth={1: 1})
    c = x.map_overlap(lambda x: x, depth={0: 1, 1: 1})

    assert len(a.dask) == len(b.dask)
    assert len(a.dask) < len(c.dask)

    assert len(c.dask) < 10 * len(a.dask)
