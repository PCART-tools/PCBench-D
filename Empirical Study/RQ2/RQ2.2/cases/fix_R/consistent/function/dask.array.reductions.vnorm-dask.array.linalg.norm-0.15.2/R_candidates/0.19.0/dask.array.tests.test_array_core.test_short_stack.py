def test_short_stack():
    x = np.array([1])
    d = da.from_array(x, chunks=(1,))
    s = da.stack([d])
    assert s.shape == (1, 1)
    chunks = compute_as_if_collection(Array, s.dask, s.__dask_keys__())
    assert chunks[0][0].shape == (1, 1)
