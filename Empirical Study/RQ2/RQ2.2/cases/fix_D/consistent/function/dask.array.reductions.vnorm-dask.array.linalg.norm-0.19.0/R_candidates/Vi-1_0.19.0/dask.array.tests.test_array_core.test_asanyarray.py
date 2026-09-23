def test_asanyarray():
    x = np.matrix([1, 2, 3])
    dx = da.asanyarray(x)
    assert dx.numblocks == (1, 1)
    chunks = compute_as_if_collection(Array, dx.dask, dx.__dask_keys__())
    assert isinstance(chunks[0][0], np.matrix)
    assert da.asanyarray(dx) is dx
