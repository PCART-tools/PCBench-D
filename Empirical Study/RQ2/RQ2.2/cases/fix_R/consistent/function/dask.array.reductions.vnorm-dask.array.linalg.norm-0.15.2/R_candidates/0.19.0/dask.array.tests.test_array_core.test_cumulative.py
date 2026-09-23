def test_cumulative():
    x = da.arange(20, chunks=5)
    assert_eq(x.cumsum(axis=0), np.arange(20).cumsum())
    assert_eq(x.cumprod(axis=0), np.arange(20).cumprod())

    assert_eq(da.nancumsum(x, axis=0), nancumsum(np.arange(20)))
    assert_eq(da.nancumprod(x, axis=0), nancumprod(np.arange(20)))

    a = np.random.random((20))
    rs = np.random.RandomState(0)
    a[rs.rand(*a.shape) < 0.5] = np.nan
    x = da.from_array(a, chunks=5)
    assert_eq(da.nancumsum(x, axis=0), nancumsum(a))
    assert_eq(da.nancumprod(x, axis=0), nancumprod(a))

    a = np.random.random((20, 24))
    x = da.from_array(a, chunks=(6, 5))
    assert_eq(x.cumsum(axis=0), a.cumsum(axis=0))
    assert_eq(x.cumsum(axis=1), a.cumsum(axis=1))
    assert_eq(x.cumprod(axis=0), a.cumprod(axis=0))
    assert_eq(x.cumprod(axis=1), a.cumprod(axis=1))

    assert_eq(da.nancumsum(x, axis=0), nancumsum(a, axis=0))
    assert_eq(da.nancumsum(x, axis=1), nancumsum(a, axis=1))
    assert_eq(da.nancumprod(x, axis=0), nancumprod(a, axis=0))
    assert_eq(da.nancumprod(x, axis=1), nancumprod(a, axis=1))

    a = np.random.random((20, 24))
    rs = np.random.RandomState(0)
    a[rs.rand(*a.shape) < 0.5] = np.nan
    x = da.from_array(a, chunks=(6, 5))
    assert_eq(da.nancumsum(x, axis=0), nancumsum(a, axis=0))
    assert_eq(da.nancumsum(x, axis=1), nancumsum(a, axis=1))
    assert_eq(da.nancumprod(x, axis=0), nancumprod(a, axis=0))
    assert_eq(da.nancumprod(x, axis=1), nancumprod(a, axis=1))

    a = np.random.random((20, 24, 13))
    x = da.from_array(a, chunks=(6, 5, 4))
    for axis in [0, 1, 2, -1, -2, -3]:
        assert_eq(x.cumsum(axis=axis), a.cumsum(axis=axis))
        assert_eq(x.cumprod(axis=axis), a.cumprod(axis=axis))

        assert_eq(da.nancumsum(x, axis=axis), nancumsum(a, axis=axis))
        assert_eq(da.nancumprod(x, axis=axis), nancumprod(a, axis=axis))

    a = np.random.random((20, 24, 13))
    rs = np.random.RandomState(0)
    a[rs.rand(*a.shape) < 0.5] = np.nan
    x = da.from_array(a, chunks=(6, 5, 4))
    for axis in [0, 1, 2, -1, -2, -3]:
        assert_eq(da.nancumsum(x, axis=axis), nancumsum(a, axis=axis))
        assert_eq(da.nancumprod(x, axis=axis), nancumprod(a, axis=axis))

    with pytest.raises(ValueError):
        x.cumsum(axis=3)

    with pytest.raises(ValueError):
        x.cumsum(axis=-4)
