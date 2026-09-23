def test_apply_gufunc_elemwise_core():
    def foo(x):
        assert x.shape == (3,)
        return 2 * x
    a = da.from_array(np.array([1, 2, 3]), chunks=3, name='a')
    z = apply_gufunc(foo, "(i)->(i)", a, output_dtypes=int)
    assert z.chunks == ((3,),)
    assert_eq(z, np.array([2, 4, 6]))
