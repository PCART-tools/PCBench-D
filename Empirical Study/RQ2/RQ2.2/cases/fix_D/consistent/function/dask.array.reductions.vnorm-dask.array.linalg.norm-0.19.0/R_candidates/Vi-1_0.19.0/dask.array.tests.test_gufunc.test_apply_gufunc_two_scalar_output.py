def test_apply_gufunc_two_scalar_output():
    def foo():
        return 1, 2
    x, y = apply_gufunc(foo, "->(),()", output_dtypes=(int, int))
    assert x.compute() == 1
    assert y.compute() == 2
