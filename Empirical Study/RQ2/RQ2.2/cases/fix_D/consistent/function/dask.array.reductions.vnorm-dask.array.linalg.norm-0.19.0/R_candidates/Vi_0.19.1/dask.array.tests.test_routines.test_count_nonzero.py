def test_count_nonzero():
    for shape, chunks in [(0, ()), ((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_c = np.count_nonzero(x)
        d_c = da.count_nonzero(d)

        if d_c.shape == tuple():
            assert x_c == d_c.compute()
        else:
            assert_eq(x_c, d_c)
