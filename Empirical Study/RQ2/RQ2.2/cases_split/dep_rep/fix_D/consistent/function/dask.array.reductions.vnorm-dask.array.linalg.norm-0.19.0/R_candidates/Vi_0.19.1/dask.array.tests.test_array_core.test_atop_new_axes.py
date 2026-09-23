def test_atop_new_axes():
    def f(x):
        return x[:, None] * np.ones((1, 7))
    x = da.ones(5, chunks=2)
    y = atop(f, 'aq', x, 'a', new_axes={'q': 7}, concatenate=True,
             dtype=x.dtype)
    assert y.chunks == ((2, 2, 1), (7,))
    assert_eq(y, np.ones((5, 7)))

    def f(x):
        return x[None, :] * np.ones((7, 1))
    x = da.ones(5, chunks=2)
    y = atop(f, 'qa', x, 'a', new_axes={'q': 7}, concatenate=True,
             dtype=x.dtype)
    assert y.chunks == ((7,), (2, 2, 1))
    assert_eq(y, np.ones((7, 5)))

    def f(x):
        y = x.sum(axis=1)
        return y[:, None] * np.ones((1, 5))

    x = da.ones((4, 6), chunks=(2, 2))
    y = atop(f, 'aq', x, 'ab', new_axes={'q': 5}, concatenate=True,
             dtype=x.dtype)
    assert y.chunks == ((2, 2), (5,))
    assert_eq(y, np.ones((4, 5)) * 6)
