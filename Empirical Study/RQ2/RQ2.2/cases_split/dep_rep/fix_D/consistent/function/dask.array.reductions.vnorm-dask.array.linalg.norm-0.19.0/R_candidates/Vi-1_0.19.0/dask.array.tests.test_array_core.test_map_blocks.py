def test_map_blocks():
    x = np.arange(400).reshape((20, 20))
    d = from_array(x, chunks=(7, 7))

    e = d.map_blocks(inc, dtype=d.dtype)

    assert d.chunks == e.chunks
    assert_eq(e, x + 1)

    e = d.map_blocks(inc, name='increment')
    assert e.name.startswith('increment-')

    assert d.map_blocks(inc, name='foo').name != d.map_blocks(dec, name='foo').name

    d = from_array(x, chunks=(10, 10))
    e = d.map_blocks(lambda x: x[::2, ::2], chunks=(5, 5), dtype=d.dtype)

    assert e.chunks == ((5, 5), (5, 5))
    assert_eq(e, x[::2, ::2])

    d = from_array(x, chunks=(8, 8))
    e = d.map_blocks(lambda x: x[::2, ::2], chunks=((4, 4, 2), (4, 4, 2)),
                     dtype=d.dtype)

    assert_eq(e, x[::2, ::2])
