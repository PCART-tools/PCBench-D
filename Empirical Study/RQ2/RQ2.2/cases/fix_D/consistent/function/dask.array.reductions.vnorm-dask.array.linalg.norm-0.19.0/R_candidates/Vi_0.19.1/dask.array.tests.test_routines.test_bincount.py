def test_bincount():
    x = np.array([2, 1, 5, 2, 1])
    d = da.from_array(x, chunks=2)
    e = da.bincount(d, minlength=6)
    assert_eq(e, np.bincount(x, minlength=6))
    assert same_keys(da.bincount(d, minlength=6), e)
