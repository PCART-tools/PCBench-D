@pytest.mark.parametrize("funcname", [
    "atleast_1d",
    "atleast_2d",
    "atleast_3d",
])
def test_atleast_nd_no_args(funcname):
    np_func = getattr(np, funcname)
    da_func = getattr(da, funcname)

    np_r_n = np_func()
    da_r_n = da_func()

    assert np_r_n == da_r_n
