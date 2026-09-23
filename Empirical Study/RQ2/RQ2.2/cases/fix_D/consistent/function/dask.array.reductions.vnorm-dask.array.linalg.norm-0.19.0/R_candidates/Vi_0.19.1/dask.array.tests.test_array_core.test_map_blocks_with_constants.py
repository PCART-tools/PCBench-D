def test_map_blocks_with_constants():
    d = da.arange(10, chunks=3)
    e = d.map_blocks(add, 100, dtype=d.dtype)

    assert_eq(e, np.arange(10) + 100)

    assert_eq(da.map_blocks(sub, d, 10, dtype=d.dtype),
              np.arange(10) - 10)
    assert_eq(da.map_blocks(sub, 10, d, dtype=d.dtype),
              10 - np.arange(10))
