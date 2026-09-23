def test_take_dask_from_numpy():
    x = np.arange(5).astype('f8')
    y = da.from_array(np.array([1, 2, 3, 3, 2 ,1]), chunks=3)

    z = da.take(x * 2, y)

    assert z.chunks == y.chunks
    assert_eq(z, np.array([2., 4., 6., 6., 4., 2.]))
