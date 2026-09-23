def test_from_array_masked_array():
    m = np.ma.masked_array([1, 2, 3], mask=[True, True, False], fill_value=10)
    dm = da.from_array(m, chunks=(2,), asarray=False)
    assert_eq(dm, m)
