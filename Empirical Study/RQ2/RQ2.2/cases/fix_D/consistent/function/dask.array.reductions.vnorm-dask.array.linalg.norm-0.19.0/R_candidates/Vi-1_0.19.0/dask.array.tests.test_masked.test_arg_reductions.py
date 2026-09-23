@pytest.mark.parametrize('reduction', ['argmin', 'argmax'])
def test_arg_reductions(reduction):
    x = np.random.random((10, 10, 10))
    dx = da.from_array(x, chunks=(3, 4, 5))
    mx = np.ma.masked_greater(x, 0.4)
    dmx = da.ma.masked_greater(dx, 0.4)

    dfunc = getattr(da, reduction)
    func = getattr(np, reduction)

    assert_eq_ma(dfunc(dmx), func(mx))
    assert_eq_ma(dfunc(dmx, 0), func(mx, 0))
    assert_eq_ma(dfunc(dmx, 1), func(mx, 1))
    assert_eq_ma(dfunc(dmx, 2), func(mx, 2))
