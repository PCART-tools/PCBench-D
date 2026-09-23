def test_apply_gufunc_elemwise_01b():
    def add(x, y):
        return x + y
    a = da.from_array(np.array([1, 2, 3]), chunks=2, name='a')
    b = da.from_array(np.array([1, 2, 3]), chunks=1, name='b')
    with pytest.raises(ValueError):
        apply_gufunc(add, "(),()->()", a, b, output_dtypes=a.dtype)
