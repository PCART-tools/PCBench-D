@pytest.mark.parametrize('func', functions)
def test_basic(func):
    x = da.random.random((2, 3, 4), chunks=(1, 2, 2))
    x[x < 0.4] = 0

    y = da.ma.masked_equal(x, 0)

    xx = func(x)
    yy = func(y)

    assert_eq(xx, da.ma.filled(yy, 0))

    if yy.shape:
        zz = yy.compute()
        assert isinstance(zz, np.ma.masked_array)
