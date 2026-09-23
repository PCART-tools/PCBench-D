def test_optimize_fuse_keys():
    x = da.ones(10, chunks=(5,))
    y = x + 1
    z = y + 1

    dsk = z.__dask_optimize__(z.dask, z.__dask_keys__())
    assert not set(y.dask) & set(dsk)

    dsk = z.__dask_optimize__(z.dask, z.__dask_keys__(),
                              fuse_keys=y.__dask_keys__())
    assert all(k in dsk for k in y.__dask_keys__())
