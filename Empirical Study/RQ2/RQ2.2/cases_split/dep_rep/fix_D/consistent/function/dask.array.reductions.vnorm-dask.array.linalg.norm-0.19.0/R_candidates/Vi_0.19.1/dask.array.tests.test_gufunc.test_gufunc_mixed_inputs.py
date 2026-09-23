def test_gufunc_mixed_inputs():
    def foo(x, y):
        return x + y
    a = np.ones((2, 1), dtype=int)
    b = da.ones((1, 8), chunks=(2, 3), dtype=int)
    x = apply_gufunc(foo, "(),()->()", a, b, output_dtypes=int)
    assert_eq(x, 2 * np.ones((2, 8), dtype=int))
