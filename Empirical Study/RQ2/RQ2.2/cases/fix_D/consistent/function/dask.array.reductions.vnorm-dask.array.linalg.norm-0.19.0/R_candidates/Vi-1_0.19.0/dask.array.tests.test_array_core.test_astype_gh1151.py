def test_astype_gh1151():
    a = np.arange(5).astype(np.int32)
    b = da.from_array(a, (1,))
    assert_eq(a.astype(np.int16), b.astype(np.int16))
