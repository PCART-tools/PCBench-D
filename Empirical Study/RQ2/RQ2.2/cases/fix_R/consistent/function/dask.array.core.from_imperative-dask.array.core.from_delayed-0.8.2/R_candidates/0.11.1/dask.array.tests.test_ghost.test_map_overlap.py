def test_map_overlap():
    x = da.arange(10, chunks=5)

    y = x.map_overlap(lambda x: x + len(x), depth=2, dtype=x._dtype)
    assert_eq(y, np.arange(10) + 5 + 2 + 2)

    x = np.arange(16).reshape((4, 4))
    d = da.from_array(x, chunks=(2, 2))
    exp1 = d.map_overlap(lambda x: x + x.size, depth=1, dtype=d._dtype)
    exp2 = d.map_overlap(lambda x: x + x.size, depth={0: 1, 1: 1},
                    boundary={0: 'reflect', 1: 'none'}, dtype=d._dtype)
    assert_eq(exp1, x + 16)
    assert_eq(exp2, x + 12)
