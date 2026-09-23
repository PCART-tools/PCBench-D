def test_atop_with_numpy_arrays():
    x = np.ones(10)
    y = da.ones(10, chunks=(5,))

    assert_eq(x + y, x + x)

    s = da.sum(x)
    assert any(x is v for v in s.dask.values())
