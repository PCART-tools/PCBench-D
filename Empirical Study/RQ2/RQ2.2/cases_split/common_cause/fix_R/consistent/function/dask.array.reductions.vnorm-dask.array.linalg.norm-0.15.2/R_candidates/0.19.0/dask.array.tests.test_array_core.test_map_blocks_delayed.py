def test_map_blocks_delayed():
    x = da.ones((10, 10), chunks=(5, 5))
    y = np.ones((5, 5))

    z = x.map_blocks(add, y, dtype=x.dtype)

    yy = delayed(y)
    zz = x.map_blocks(add, yy, dtype=x.dtype)

    assert_eq(z, zz)

    assert yy.key in zz.dask
