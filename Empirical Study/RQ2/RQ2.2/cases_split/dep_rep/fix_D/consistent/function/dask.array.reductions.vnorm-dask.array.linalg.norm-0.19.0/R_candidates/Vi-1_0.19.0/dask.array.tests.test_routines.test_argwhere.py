def test_argwhere():
    for shape, chunks in [(0, ()), ((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_nz = np.argwhere(x)
        d_nz = da.argwhere(d)

        assert_eq(d_nz, x_nz)
