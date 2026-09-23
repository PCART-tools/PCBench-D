def test_dont_fuse_different_slices():
    x = da.random.random(size=(10, 10), chunks=(10, 1))
    y = x.rechunk((1, 10))
    dsk = optimize(y.dask, y._keys())
    assert len(dsk) > 100
