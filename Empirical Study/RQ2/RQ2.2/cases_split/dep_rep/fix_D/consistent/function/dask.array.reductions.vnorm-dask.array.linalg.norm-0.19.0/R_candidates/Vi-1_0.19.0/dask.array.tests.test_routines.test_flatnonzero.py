def test_flatnonzero():
    for shape, chunks in [(0, ()), ((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_fnz = np.flatnonzero(x)
        d_fnz = da.flatnonzero(d)

        assert_eq(d_fnz, x_fnz)
