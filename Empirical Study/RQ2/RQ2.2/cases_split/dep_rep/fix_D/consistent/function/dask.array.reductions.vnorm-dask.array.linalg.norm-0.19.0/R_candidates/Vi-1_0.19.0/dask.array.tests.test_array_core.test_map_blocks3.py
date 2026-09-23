def test_map_blocks3():
    x = np.arange(10)
    y = np.arange(10) * 2

    d = da.from_array(x, chunks=5)
    e = da.from_array(y, chunks=5)

    assert_eq(da.core.map_blocks(lambda a, b: a + 2 * b, d, e, dtype=d.dtype),
              x + 2 * y)

    z = np.arange(100).reshape((10, 10))
    f = da.from_array(z, chunks=5)

    func = lambda a, b: a + 2 * b
    res = da.core.map_blocks(func, d, f, dtype=d.dtype)
    assert_eq(res, x + 2 * z)
    assert same_keys(da.core.map_blocks(func, d, f, dtype=d.dtype), res)

    assert_eq(da.map_blocks(func, f, d, dtype=d.dtype), z + 2 * x)
