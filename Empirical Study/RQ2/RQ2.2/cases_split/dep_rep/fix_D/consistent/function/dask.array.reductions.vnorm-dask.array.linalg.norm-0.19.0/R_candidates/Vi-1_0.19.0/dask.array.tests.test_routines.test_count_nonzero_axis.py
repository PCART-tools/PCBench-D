@pytest.mark.skipif(LooseVersion(np.__version__) < '1.12.0',
                    reason="NumPy's count_nonzero doesn't yet support axis")
@pytest.mark.parametrize('axis', [None, 0, (1,), (0, 1)])
def test_count_nonzero_axis(axis):
    for shape, chunks in [((0, 0), (0, 0)), ((15, 16), (4, 5))]:
        x = np.random.randint(10, size=shape)
        d = da.from_array(x, chunks=chunks)

        x_c = np.count_nonzero(x, axis)
        d_c = da.count_nonzero(d, axis)

        if d_c.shape == tuple():
            assert x_c == d_c.compute()
        else:
            assert_eq(x_c, d_c)
