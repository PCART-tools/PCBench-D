def test_dont_fuse_numpy_arrays():
    x = np.ones(10)
    for chunks in [(5,), (10,)]:
        y = da.from_array(x, chunks=(10,))

        dsk = y.__dask_optimize__(y.dask, y.__dask_keys__())
        assert sum(isinstance(v, np.ndarray) for v in dsk.values()) == 1
