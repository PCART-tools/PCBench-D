def test_apply_gufunc_check_same_dimsizes():
    def foo(x, y):
        return x + y

    a = da.random.normal(size=(3,), chunks=(2,))
    b = da.random.normal(size=(4,), chunks=(2,))

    with pytest.raises(ValueError) as excinfo:
        apply_gufunc(foo, "(),()->()", a, b, output_dtypes=float, allow_rechunk=True)
    assert "different lengths in arrays" in str(excinfo.value)
