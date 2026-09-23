def test_apply_gufunc_check_inhomogeneous_chunksize():
    def foo(x, y):
        return x + y

    a = da.random.normal(size=(8,), chunks=((2, 2, 2, 2),))
    b = da.random.normal(size=(8,), chunks=((2, 3, 3),))

    with pytest.raises(ValueError) as excinfo:
        da.apply_gufunc(foo, "(),()->()", a, b, output_dtypes=float, allow_rechunk=False)
    assert "with different chunksize present" in str(excinfo.value)
