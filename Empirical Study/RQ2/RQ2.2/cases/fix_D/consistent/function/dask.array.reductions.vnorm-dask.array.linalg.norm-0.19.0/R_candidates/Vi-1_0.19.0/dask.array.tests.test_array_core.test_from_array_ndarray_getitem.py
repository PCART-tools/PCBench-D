def test_from_array_ndarray_getitem():
    """For ndarray, don't use getter / getter_nofancy; use the cleaner
    operator.getitem"""
    x = np.array([[1, 2], [3, 4]])
    dx = da.from_array(x, chunks=(1, 2))
    assert_eq(x, dx)
    assert dx.dask[dx.name, 0, 0][0] == operator.getitem
