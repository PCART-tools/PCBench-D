def test_apply_gufunc_two_mixed_outputs():
    def foo():
        return 1, np.ones((2, 3), dtype=float)
    x, y = apply_gufunc(foo, "->(),(i,j)",
                        output_dtypes=(int, float),
                        output_sizes={'i': 2, 'j': 3})
    assert x.compute() == 1
    assert y.chunks == ((2,), (3,))
    assert_eq(y, np.ones((2, 3), dtype=float))
