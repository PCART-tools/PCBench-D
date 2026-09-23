def test_uneven_chunks_that_fit_neatly():
    x = da.arange(10, chunks=((5, 5),))
    y = da.ones(10, chunks=((5, 2, 3),))

    assert_eq(x + y, np.arange(10) + np.ones(10))

    z = x + y
    assert z.chunks == ((5, 2, 3),)
