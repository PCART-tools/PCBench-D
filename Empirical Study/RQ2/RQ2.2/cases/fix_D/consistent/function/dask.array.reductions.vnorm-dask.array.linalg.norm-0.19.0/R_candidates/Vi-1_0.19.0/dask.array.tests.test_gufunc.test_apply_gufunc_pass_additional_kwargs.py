def test_apply_gufunc_pass_additional_kwargs():
    def foo(x, bar):
        assert bar == 2
        return x
    ret = apply_gufunc(foo, "()->()", 1., output_dtypes="f", bar=2)
    assert_eq(ret, np.array(1., dtype="f"))
