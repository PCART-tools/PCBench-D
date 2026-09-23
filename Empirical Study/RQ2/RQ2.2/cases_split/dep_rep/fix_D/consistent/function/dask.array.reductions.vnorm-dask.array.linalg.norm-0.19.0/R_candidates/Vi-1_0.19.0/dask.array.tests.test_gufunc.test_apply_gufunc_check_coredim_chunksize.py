def test_apply_gufunc_check_coredim_chunksize():
    def foo(x):
        return np.sum(x, axis=-1)
    a = da.random.normal(size=(8,), chunks=3)
    with pytest.raises(ValueError) as excinfo:
        da.apply_gufunc(foo, "(i)->()", a, output_dtypes=float, allow_rechunk=False)
    assert "consists of multiple chunks" in str(excinfo.value)
