def test_concatenate_rechunk():
    x = da.random.random((6, 6), chunks=(3, 3))
    y = da.random.random((6, 6), chunks=(2, 2))

    z = da.concatenate([x, y], axis=0)
    assert z.shape == (12, 6)
    assert z.chunks == ((3, 3, 2, 2, 2), (2, 1, 1, 2))
    assert_eq(z, np.concatenate([x.compute(), y.compute()], axis=0))

    z = da.concatenate([x, y], axis=1)
    assert z.shape == (6, 12)
    assert z.chunks == ((2, 1, 1, 2), (3, 3, 2, 2, 2))
    assert_eq(z, np.concatenate([x.compute(), y.compute()], axis=1))
