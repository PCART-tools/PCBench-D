@pytest.mark.xfail(reason="Currently np.einsum doesn't seem to broadcast correctly for this case")
def test_apply_gufunc_02():
    def outer_product(x, y):
        return np.einsum("...i,...j->...ij", x, y)
    a = da.random.normal(size=(   20, 30), chunks=(5, 30))
    b = da.random.normal(size=(10, 1, 40), chunks=(10, 1, 40))
    c = apply_gufunc(outer_product, "(i),(j)->(i,j)", a, b, output_dtypes=a.dtype)
    assert c.compute().shape == (10, 20, 30, 40)
