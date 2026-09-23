@pytest.mark.parametrize("funcname", [
    "atleast_1d",
    "atleast_2d",
    "atleast_3d",
])
@pytest.mark.parametrize("shape, chunks", [
    (tuple(), tuple()),
    ((4,), (2,)),
    ((4, 6), (2, 3)),
    ((4, 6, 8), (2, 3, 4)),
    ((4, 6, 8, 10), (2, 3, 4, 5)),
])
def test_atleast_nd_one_arg(funcname, shape, chunks):
    np_a = np.random.random(shape)
    da_a = da.from_array(np_a, chunks=chunks)

    np_func = getattr(np, funcname)
    da_func = getattr(da, funcname)

    np_r = np_func(np_a)
    da_r = da_func(da_a)

    assert_eq(np_r, da_r)
