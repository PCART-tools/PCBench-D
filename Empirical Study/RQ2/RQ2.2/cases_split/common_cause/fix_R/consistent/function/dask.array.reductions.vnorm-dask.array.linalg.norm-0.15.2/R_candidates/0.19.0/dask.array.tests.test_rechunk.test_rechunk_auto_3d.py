def test_rechunk_auto_3d():
    x = da.ones((20, 20, 20), chunks=((2, 2, 2)))
    y = x.rechunk({0: 'auto', 1: 'auto'}, block_size_limit=200 * x.dtype.itemsize)
    assert y.chunks[2] == x.chunks[2]
    assert y.chunks[0] == (10, 10)
    assert y.chunks[1] == (10, 10)  # even split
