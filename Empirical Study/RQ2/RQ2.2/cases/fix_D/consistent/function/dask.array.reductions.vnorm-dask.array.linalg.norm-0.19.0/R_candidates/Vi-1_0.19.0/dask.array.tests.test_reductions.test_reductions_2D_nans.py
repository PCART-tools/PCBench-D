def test_reductions_2D_nans():
    # chunks are a mix of some/all/no NaNs
    x = np.full((4, 4), np.nan)
    x[:2, :2] = np.array([[1, 2], [3, 4]])
    x[2, 2] = 5
    x[3, 3] = 6
    a = da.from_array(x, chunks=(2, 2))

    reduction_2d_test(da.sum, a, np.sum, x, False, False)
    reduction_2d_test(da.prod, a, np.prod, x, False, False)
    reduction_2d_test(da.mean, a, np.mean, x, False, False)
    reduction_2d_test(da.var, a, np.var, x, False, False)
    reduction_2d_test(da.std, a, np.std, x, False, False)
    reduction_2d_test(da.min, a, np.min, x, False, False)
    reduction_2d_test(da.max, a, np.max, x, False, False)
    reduction_2d_test(da.any, a, np.any, x, False, False)
    reduction_2d_test(da.all, a, np.all, x, False, False)

    reduction_2d_test(da.nansum, a, np.nansum, x, False, False)
    reduction_2d_test(da.nanprod, a, np.nanprod, x, False, False)
    reduction_2d_test(da.nanmean, a, np.nanmean, x, False, False)
    with pytest.warns(None):  # division by 0 warning
        reduction_2d_test(da.nanvar, a, np.nanvar, x, False, False)
    with pytest.warns(None):  # division by 0 warning
        reduction_2d_test(da.nanstd, a, np.nanstd, x, False, False)
    with pytest.warns(None):  # all NaN axis warning
        reduction_2d_test(da.nanmin, a, np.nanmin, x, False, False)
    with pytest.warns(None):  # all NaN axis warning
        reduction_2d_test(da.nanmax, a, np.nanmax, x, False, False)

    assert_eq(da.argmax(a), np.argmax(x))
    assert_eq(da.argmin(a), np.argmin(x))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmax(a), np.nanargmax(x))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmin(a), np.nanargmin(x))
    assert_eq(da.argmax(a, axis=0), np.argmax(x, axis=0))
    assert_eq(da.argmin(a, axis=0), np.argmin(x, axis=0))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmax(a, axis=0), np.nanargmax(x, axis=0))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmin(a, axis=0), np.nanargmin(x, axis=0))
    assert_eq(da.argmax(a, axis=1), np.argmax(x, axis=1))
    assert_eq(da.argmin(a, axis=1), np.argmin(x, axis=1))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmax(a, axis=1), np.nanargmax(x, axis=1))
    with pytest.warns(None):  # all NaN axis warning
        assert_eq(da.nanargmin(a, axis=1), np.nanargmin(x, axis=1))
