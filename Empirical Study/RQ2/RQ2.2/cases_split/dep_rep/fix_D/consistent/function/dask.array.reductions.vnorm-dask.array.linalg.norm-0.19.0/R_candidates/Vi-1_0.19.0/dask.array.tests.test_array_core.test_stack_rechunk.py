def test_stack_rechunk():
    x = da.random.random(10, chunks=5)
    y = da.random.random(10, chunks=4)

    z = da.stack([x, y], axis=0)
    assert z.shape == (2, 10)
    assert z.chunks == ((1, 1), (4, 1, 3, 2))

    assert_eq(z, np.stack([x.compute(), y.compute()], axis=0))
