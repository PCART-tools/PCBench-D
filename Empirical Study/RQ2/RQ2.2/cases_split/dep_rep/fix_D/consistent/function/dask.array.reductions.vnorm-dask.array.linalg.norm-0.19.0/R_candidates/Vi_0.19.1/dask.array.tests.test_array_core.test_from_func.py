def test_from_func():
    x = np.arange(10)
    f = lambda n: n * x
    d = from_func(f, (10,), x.dtype, kwargs={'n': 2})

    assert d.shape == x.shape
    assert d.dtype == x.dtype
    assert_eq(d.compute(), 2 * x)
    assert same_keys(d, from_func(f, (10,), x.dtype, kwargs={'n': 2}))
