def test_apply_gufunc_scalar_output():
    def foo():
        return 1
    x = apply_gufunc(foo, "->()", output_dtypes=int)
    assert x.compute() == 1
