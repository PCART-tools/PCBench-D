def test_nonzero():
    for shape, chunks in [(0, ()), ((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_nz = np.nonzero(x)
        d_nz = da.nonzero(d)

        assert isinstance(d_nz, type(x_nz))
        assert len(d_nz) == len(x_nz)

        for i in range(len(x_nz)):
            assert_eq(d_nz[i], x_nz[i])
