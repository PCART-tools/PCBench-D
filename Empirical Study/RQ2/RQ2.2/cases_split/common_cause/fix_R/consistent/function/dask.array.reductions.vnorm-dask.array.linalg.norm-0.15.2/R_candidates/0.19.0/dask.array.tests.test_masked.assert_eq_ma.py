def assert_eq_ma(a, b):
    res = a.compute()
    assert type(res) == type(b)
    if hasattr(res, 'mask'):
        np.testing.assert_equal(res.mask, b.mask)
        a = da.ma.filled(a)
        b = np.ma.filled(b)
    assert_eq(a, b, equal_nan=True)
