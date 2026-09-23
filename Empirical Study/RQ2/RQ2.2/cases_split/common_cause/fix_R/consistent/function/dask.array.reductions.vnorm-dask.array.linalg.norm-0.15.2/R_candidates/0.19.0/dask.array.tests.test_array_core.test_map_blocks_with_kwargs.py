def test_map_blocks_with_kwargs():
    d = da.arange(10, chunks=5)

    result = d.map_blocks(np.max, axis=0, keepdims=True, dtype=d.dtype,
                          chunks=(1,))

    assert_eq(result, np.array([4, 9]))
