def test_uneven_chunks_atop():
    x = da.random.random((10, 10), chunks=((2, 3, 2, 3), (5, 5)))
    y = da.random.random((10, 10), chunks=((4, 4, 2), (4, 2, 4)))
    z = atop(np.dot, 'ik', x, 'ij', y, 'jk', dtype=x.dtype, concatenate=True)
    assert z.chunks == (x.chunks[0], y.chunks[1])

    assert_eq(z, x.compute().dot(y))
