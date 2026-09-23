def test_cov():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(4, 4))

    assert_eq(da.cov(d), np.cov(x))
    assert_eq(da.cov(d, rowvar=0), np.cov(x, rowvar=0))
    with pytest.warns(None):  # warning dof <= 0 for slice
        assert_eq(da.cov(d, ddof=10), np.cov(x, ddof=10))
    assert_eq(da.cov(d, bias=1), np.cov(x, bias=1))
    assert_eq(da.cov(d, d), np.cov(x, x))

    y = np.arange(8)
    e = da.from_array(y, chunks=(4,))

    assert_eq(da.cov(d, e), np.cov(x, y))
    assert_eq(da.cov(e, d), np.cov(y, x))

    with pytest.raises(ValueError):
        da.cov(d, ddof=1.5)
