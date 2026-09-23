def test_apply_gufunc_elemwise_01():
    def add(x, y):
        return x + y
    a = da.from_array(np.array([1, 2, 3]), chunks=2, name='a')
    b = da.from_array(np.array([1, 2, 3]), chunks=2, name='b')
    z = apply_gufunc(add, "(),()->()", a, b, output_dtypes=a.dtype)
    assert_eq(z, np.array([2, 4, 6]))
