def test_tensordot():
    x = da.random.random((2, 3, 4), chunks=(1, 2, 2))
    x[x < 0.4] = 0
    y = da.random.random((4, 3, 2), chunks=(2, 2, 1))
    y[y < 0.4] = 0

    xx = da.ma.masked_equal(x, 0)
    yy = da.ma.masked_equal(y, 0)

    assert_eq(da.tensordot(x, y, axes=(2, 0)),
              da.ma.filled(da.tensordot(xx, yy, axes=(2, 0)), 0))
    assert_eq(da.tensordot(x, y, axes=(1, 1)),
              da.ma.filled(da.tensordot(xx, yy, axes=(1, 1)), 0))
    assert_eq(da.tensordot(x, y, axes=((1, 2), (1, 0))),
              da.ma.filled(da.tensordot(xx, yy, axes=((1, 2), (1, 0))), 0))
