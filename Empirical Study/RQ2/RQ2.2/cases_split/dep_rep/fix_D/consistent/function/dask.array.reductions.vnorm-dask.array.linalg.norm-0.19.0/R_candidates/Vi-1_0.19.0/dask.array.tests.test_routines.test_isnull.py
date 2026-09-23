def test_isnull():
    x = np.array([1, np.nan])
    a = da.from_array(x, chunks=(2,))
    with ignoring(ImportError):
        assert_eq(da.isnull(a), np.isnan(x))
        assert_eq(da.notnull(a), ~np.isnan(x))
