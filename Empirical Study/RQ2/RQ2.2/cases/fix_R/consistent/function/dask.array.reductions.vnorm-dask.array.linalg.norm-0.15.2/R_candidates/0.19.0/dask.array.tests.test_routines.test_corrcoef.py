def test_corrcoef():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(4, 4))

    assert_eq(da.corrcoef(d), np.corrcoef(x))
    assert_eq(da.corrcoef(d, rowvar=0), np.corrcoef(x, rowvar=0))
    assert_eq(da.corrcoef(d, d), np.corrcoef(x, x))

    y = np.arange(8)
    e = da.from_array(y, chunks=(4,))

    assert_eq(da.corrcoef(d, e), np.corrcoef(x, y))
    assert_eq(da.corrcoef(e, d), np.corrcoef(y, x))
