def test_map_overlap():
    x = da.arange(10, chunks=5)
    y = x.map_overlap(lambda x: x + len(x), depth=2, dtype=x.dtype)
    assert_eq(y, np.arange(10) + 5 + 2 + 2)

    x = da.arange(10, chunks=5)
    y = x.map_overlap(lambda x: x + len(x), depth=np.int64(2), dtype=x.dtype)
    assert all([(type(s) is int) for s in y.shape])
    assert_eq(y, np.arange(10) + 5 + 2 + 2)

    x = np.arange(16).reshape((4, 4))
    d = da.from_array(x, chunks=(2, 2))
    exp1 = d.map_overlap(lambda x: x + x.size, depth=1, dtype=d.dtype)
    exp2 = d.map_overlap(lambda x: x + x.size, depth={0: 1, 1: 1},
                         boundary={0: 'reflect', 1: 'none'}, dtype=d.dtype)
    exp3 = d.map_overlap(lambda x: x + x.size, depth={1: 1},
                         boundary={1: 'reflect'}, dtype=d.dtype)
    assert_eq(exp1, x + 16)
    assert_eq(exp2, x + 12)
    assert_eq(exp3, x + 8)
