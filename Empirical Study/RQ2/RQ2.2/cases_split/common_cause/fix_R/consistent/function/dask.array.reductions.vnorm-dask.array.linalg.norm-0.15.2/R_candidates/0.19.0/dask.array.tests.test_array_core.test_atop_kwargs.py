def test_atop_kwargs():
    def f(a, b=0):
        return a + b

    x = da.ones(5, chunks=(2,))
    y = atop(f, 'i', x, 'i', b=10, dtype=x.dtype)
    assert_eq(y, np.ones(5) + 10)
