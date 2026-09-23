@pytest.mark.parametrize("func", ["cumsum", "cumprod"])
@pytest.mark.parametrize("axis", [None, 0, 1, -1])
def test_array_cumreduction_axis(func, axis):
    np_func = getattr(np, func)
    da_func = getattr(da, func)

    s = (10, 11, 12)
    a = np.arange(np.prod(s)).reshape(s)
    d = da.from_array(a, chunks=(4, 5, 6))

    a_r = np_func(a, axis=axis)
    d_r = da_func(d, axis=axis)

    assert_eq(a_r, d_r)
