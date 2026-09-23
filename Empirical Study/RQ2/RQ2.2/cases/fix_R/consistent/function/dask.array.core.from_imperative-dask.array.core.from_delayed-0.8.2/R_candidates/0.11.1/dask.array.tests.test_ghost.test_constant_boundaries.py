def test_constant_boundaries():
    a = np.arange(1 * 9).reshape(1, 9)
    darr = da.from_array(a, chunks=((1,), (2, 2, 2, 3)))
    b = boundaries(darr, {0: 0, 1: 0}, {0: 0, 1: 0})
    assert b.chunks == darr.chunks
