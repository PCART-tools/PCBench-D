def test_asarray():
    assert_eq(da.asarray([1, 2, 3]), np.asarray([1, 2, 3]))

    x = da.asarray([1, 2, 3])
    assert da.asarray(x) is x
