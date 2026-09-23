def test_map_blocks2():
    x = np.arange(10, dtype='i8')
    d = from_array(x, chunks=(2,))

    def func(block, block_id=None, c=0):
        return np.ones_like(block) * sum(block_id) + c

    out = d.map_blocks(func, dtype='i8')
    expected = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4], dtype='i8')

    assert_eq(out, expected)
    assert same_keys(d.map_blocks(func, dtype='i8'), out)

    out = d.map_blocks(func, dtype='i8', c=1)
    expected = expected + 1

    assert_eq(out, expected)
    assert same_keys(d.map_blocks(func, dtype='i8', c=1), out)
