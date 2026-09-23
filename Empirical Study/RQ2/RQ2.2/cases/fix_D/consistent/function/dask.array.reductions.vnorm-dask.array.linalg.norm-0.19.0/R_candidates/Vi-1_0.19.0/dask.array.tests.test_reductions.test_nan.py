def test_nan():
    x = np.array([[1, np.nan, 3, 4],
                  [5, 6, 7, np.nan],
                  [9, 10, 11, 12]])
    d = da.from_array(x, chunks=(2, 2))

    assert_eq(np.nansum(x), da.nansum(d))
    assert_eq(np.nansum(x, axis=0), da.nansum(d, axis=0))
    assert_eq(np.nanmean(x, axis=1), da.nanmean(d, axis=1))
    assert_eq(np.nanmin(x, axis=1), da.nanmin(d, axis=1))
    assert_eq(np.nanmax(x, axis=(0, 1)), da.nanmax(d, axis=(0, 1)))
    assert_eq(np.nanvar(x), da.nanvar(d))
    assert_eq(np.nanstd(x, axis=0), da.nanstd(d, axis=0))
    assert_eq(np.nanargmin(x, axis=0), da.nanargmin(d, axis=0))
    assert_eq(np.nanargmax(x, axis=0), da.nanargmax(d, axis=0))
    assert_eq(np.nanprod(x), da.nanprod(d))
