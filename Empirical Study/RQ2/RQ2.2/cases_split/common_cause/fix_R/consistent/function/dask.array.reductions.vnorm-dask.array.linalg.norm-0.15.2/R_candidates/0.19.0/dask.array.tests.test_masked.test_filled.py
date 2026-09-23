def test_filled():
    x = np.array([-2, -1, 0, 1, 2] * 20).reshape((10, 10))
    dx = da.from_array(x, chunks=5)

    mx = np.ma.masked_equal(x, 0)
    mdx = da.ma.masked_equal(dx, 0)

    assert_eq(da.ma.filled(mdx), np.ma.filled(mx))
    assert_eq(da.ma.filled(mdx, -5), np.ma.filled(mx, -5))
