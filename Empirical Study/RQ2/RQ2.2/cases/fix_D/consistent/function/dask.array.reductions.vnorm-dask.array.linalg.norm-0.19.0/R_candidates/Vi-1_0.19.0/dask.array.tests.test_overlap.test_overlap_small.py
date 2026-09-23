def test_overlap_small():
    x = da.ones((10, 10), chunks=(5, 5))

    y = x.map_overlap(lambda x: x, depth=1)
    assert len(y.dask) < 200

    y = x.map_overlap(lambda x: x, depth=1, boundary='none')
    assert len(y.dask) < 100
