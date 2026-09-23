def test_from_array_ndarray_onechunk():
    """ndarray with a single chunk produces a minimal single key dict
    """
    x = np.array([[1, 2], [3, 4]])
    dx = da.from_array(x, chunks=-1)
    assert_eq(x, dx)
    assert len(dx.dask) == 1
    assert dx.dask[dx.name, 0, 0] is x
