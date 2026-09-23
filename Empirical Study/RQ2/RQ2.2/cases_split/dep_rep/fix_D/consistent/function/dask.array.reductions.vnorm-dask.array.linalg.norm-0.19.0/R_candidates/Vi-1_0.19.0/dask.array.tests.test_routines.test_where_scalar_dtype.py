def test_where_scalar_dtype():
    x = np.int32(3)
    y1 = np.array([4, 5, 6], dtype=np.int16)
    c1 = np.array([1, 0, 1])
    y2 = da.from_array(y1, chunks=2)
    c2 = da.from_array(c1, chunks=2)
    w1 = np.where(c1, x, y1)
    w2 = da.where(c2, x, y2)
    assert_eq(w1, w2)
    # Test again for the bool optimization
    w3 = np.where(True, x, y1)
    w4 = da.where(True, x, y1)
    assert_eq(w3, w4)
