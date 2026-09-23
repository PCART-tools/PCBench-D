def test_choose():
    # test choose function
    x = np.random.randint(10, size=(15, 16))
    d = da.from_array(x, chunks=(4, 5))

    assert_eq(da.choose(d > 5, [0, d]), np.choose(x > 5, [0, x]))
    assert_eq(da.choose(d > 5, [-d, d]), np.choose(x > 5, [-x, x]))

    # test choose method
    index_dask = d > 5
    index_numpy = x > 5
    assert_eq(index_dask.choose([0, d]), index_numpy.choose([0, x]))
    assert_eq(index_dask.choose([-d, d]), index_numpy.choose([-x, x]))
