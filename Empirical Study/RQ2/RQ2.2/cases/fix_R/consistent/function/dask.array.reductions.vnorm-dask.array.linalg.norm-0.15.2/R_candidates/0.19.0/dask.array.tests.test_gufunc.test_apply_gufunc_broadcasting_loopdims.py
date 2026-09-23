def test_apply_gufunc_broadcasting_loopdims():
    def foo(x, y):
        assert len(x.shape) == 2
        assert len(y.shape) == 3
        x, y = np.broadcast_arrays(x, y)
        return x, y, x * y

    a = da.random.normal(size=(    10, 30), chunks=(8, 30))
    b = da.random.normal(size=(20,  1, 30), chunks=(3, 1, 30))

    x, y, z = apply_gufunc(foo, "(i),(i)->(i),(i),(i)", a, b, output_dtypes=3 * (float,), vectorize=False)

    assert x.compute().shape == (20, 10, 30)
    assert y.compute().shape == (20, 10, 30)
    assert z.compute().shape == (20, 10, 30)
