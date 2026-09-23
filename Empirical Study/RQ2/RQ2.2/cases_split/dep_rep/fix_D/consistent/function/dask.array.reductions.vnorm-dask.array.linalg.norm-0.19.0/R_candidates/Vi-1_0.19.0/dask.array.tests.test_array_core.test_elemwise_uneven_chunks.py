def test_elemwise_uneven_chunks():
    x = da.arange(10, chunks=((4, 6),))
    y = da.ones(10, chunks=((6, 4),))

    assert_eq(x + y, np.arange(10) + np.ones(10))

    z = x + y
    assert z.chunks == ((4, 2, 4),)

    x = da.random.random((10, 10), chunks=((4, 6), (5, 2, 3)))
    y = da.random.random((4, 10, 10), chunks=((2, 2), (6, 4), (2, 3, 5)))

    z = x + y
    assert_eq(x + y, x.compute() + y.compute())
    assert z.chunks == ((2, 2), (4, 2, 4), (2, 3, 2, 3))
