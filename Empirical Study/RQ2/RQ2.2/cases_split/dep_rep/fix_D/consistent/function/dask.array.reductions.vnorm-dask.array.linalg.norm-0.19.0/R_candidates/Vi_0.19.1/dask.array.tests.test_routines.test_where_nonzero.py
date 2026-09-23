def test_where_nonzero():
    for shape, chunks in [(0, ()), ((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_w = np.where(x)
        d_w = da.where(d)

        assert isinstance(d_w, type(x_w))
        assert len(d_w) == len(x_w)

        for i in range(len(x_w)):
            assert_eq(d_w[i], x_w[i])
