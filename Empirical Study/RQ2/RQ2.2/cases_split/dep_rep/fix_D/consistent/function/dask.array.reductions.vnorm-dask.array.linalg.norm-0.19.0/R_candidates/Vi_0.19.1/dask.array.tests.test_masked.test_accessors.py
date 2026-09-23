def test_accessors():
    x = np.random.random((10, 10))
    dx = da.from_array(x, chunks=(3, 4))
    mx = np.ma.masked_greater(x, 0.4)
    dmx = da.ma.masked_greater(dx, 0.4)

    assert_eq(da.ma.getmaskarray(dmx), np.ma.getmaskarray(mx))
    assert_eq(da.ma.getmaskarray(dx), np.ma.getmaskarray(x))
    assert_eq(da.ma.getdata(dmx), np.ma.getdata(mx))
    assert_eq(da.ma.getdata(dx), np.ma.getdata(x))
