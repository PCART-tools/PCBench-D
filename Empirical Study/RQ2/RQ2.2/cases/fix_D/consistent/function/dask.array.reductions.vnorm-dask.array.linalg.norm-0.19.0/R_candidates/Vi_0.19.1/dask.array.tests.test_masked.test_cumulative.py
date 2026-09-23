def test_cumulative():
    x = np.random.RandomState(0).rand(20, 24, 13)
    dx = da.from_array(x, chunks=(6, 5, 4))
    mx = np.ma.masked_greater(x, 0.4)
    dmx = da.ma.masked_greater(dx, 0.4)

    for axis in [0, 1, 2]:
        assert_eq_ma(dmx.cumsum(axis=axis), mx.cumsum(axis=axis))
        assert_eq_ma(dmx.cumprod(axis=axis), mx.cumprod(axis=axis))
