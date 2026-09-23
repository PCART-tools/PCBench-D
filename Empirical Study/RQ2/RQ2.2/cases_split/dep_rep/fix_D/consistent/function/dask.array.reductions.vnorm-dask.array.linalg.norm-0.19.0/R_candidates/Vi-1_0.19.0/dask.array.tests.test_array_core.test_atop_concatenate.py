def test_atop_concatenate():
    x = da.ones((4, 4, 4), chunks=(2, 2, 2))
    y = da.ones((4, 4), chunks=(2, 2))

    def f(a, b):
        assert isinstance(a, np.ndarray)
        assert isinstance(b, np.ndarray)

        assert a.shape == (2, 4, 4)
        assert b.shape == (4, 4)

        return (a + b).sum(axis=(1, 2))

    z = atop(f, 'i', x, 'ijk', y, 'jk', concatenate=True, dtype=x.dtype)
    assert_eq(z, np.ones(4) * 32)

    z = atop(add, 'ij', y, 'ij', y, 'ij', concatenate=True, dtype=x.dtype)
    assert_eq(z, np.ones((4, 4)) * 2)

    def f(a, b, c):
        assert isinstance(a, np.ndarray)
        assert isinstance(b, np.ndarray)
        assert isinstance(c, np.ndarray)

        assert a.shape == (4, 2, 4)
        assert b.shape == (4, 4)
        assert c.shape == (4, 2)

        return np.ones(5)

    z = atop(f, 'j', x, 'ijk', y, 'ki', y, 'ij', concatenate=True,
             dtype=x.dtype)
    assert_eq(z, np.ones(10), check_shape=False)
