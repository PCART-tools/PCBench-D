def test_turn_off_fusion():
    x = da.ones(10, chunks=(5,))
    y = da.sum(x + 1 + 2 + 3)

    a = y.__dask_optimize__(y.dask, y.__dask_keys__())

    with dask.config.set(fuse_ave_width=0):
        b = y.__dask_optimize__(y.dask, y.__dask_keys__())

    assert dask.get(a, y.__dask_keys__()) == dask.get(b, y.__dask_keys__())
    assert len(a) < len(b)
