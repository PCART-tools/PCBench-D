def test_multinomial():
    for size, chunks in [(5, 3), ((5, 4), (2, 3))]:
        x = da.random.multinomial(20, [1 / 6.] * 6, size=size, chunks=chunks)
        y = np.random.multinomial(20, [1 / 6.] * 6, size=size)

        assert x.shape == y.shape == x.compute().shape
